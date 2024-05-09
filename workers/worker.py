import zmq
import numpy as np
import cv2
import torch
import json
from ultralytics import YOLO
from multiprocessing import Process
from threading import Thread
from skimage.metrics import peak_signal_noise_ratio
from config import config


class ThreadRet(Thread):
    """Custom Thread class allowing to return values from threads"""

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
 
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
             
    def join(self, *args):
        Thread.join(self, *args)
        return self._return
    

def predict(model, image):
    """get YOLO prediction

    Args:
        model (YOLO): YOLOv8 model
        image (MatLike): cv2 image

    Returns:
        str: results of json-like string type
    """
    result = model(image)[0]
    return result.tojson()


def worker_process(pull_addr: str, push_addr: str):
    """Make worker process

    Args:
        pull_addr (str): address to get images from
        push_addr (str): address to send images to
    """

    if torch.cuda.is_available():
        torch.cuda.set_device(0)

    forklift_model = YOLO(config['models']['forklift'])
    fire_model = YOLO(config['models']['fire'])

    context = zmq.Context()
    puller = context.socket(zmq.PULL)
    puller.bind(pull_addr)

    pusher = context.socket(zmq.PUSH)
    pusher.connect(push_addr)

    while True:
        [address, contents] = puller.recv_multipart()

        encoded_frame = np.frombuffer(contents, dtype=np.uint8)
        frame = cv2.imdecode(encoded_frame, cv2.IMREAD_COLOR)
        meanframe = cv2.imread(config['sources'][int.from_bytes(address)]['meanframe'])

        t_forklift = ThreadRet(target=predict, args=(forklift_model, frame))
        t_fire = ThreadRet(target=predict, args=(fire_model, frame))
        t_psnr = ThreadRet(target=peak_signal_noise_ratio, args=(meanframe, frame))
        t_forklift.start()
        t_fire.start()
        t_psnr.start()
        res_forklift = json.loads(t_forklift.join())
        res_fire = json.loads(t_fire.join())
        res_psnr = t_psnr.join()

        res = res_forklift + res_fire
        res = str(res).replace('\'', '\"').encode()
        
        print(f'PSNR {int.from_bytes(address)} {res_psnr}')

        data = [address, contents, res, str(round(res_psnr)).encode()]
        pusher.send_multipart(data)
    

    # We never get here but clean up anyhow
    pusher.close()
    context.term()


def main():
    for worker in config['workers']:
        Process(target=worker_process, args=(worker, config['gui'])).start()


if __name__ == "__main__":
    main()