import zmq
import cv2
from multiprocessing import Process
from time import sleep
from config import config

def start_source(id, source: dict):
    """Starts videosource process

    Args:
        id (int): defines source id
        source (dict): videosource dict having 'port' and 'path' fields
    """
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(source['port'])

    cap = cv2.VideoCapture(source['path'])
    count = 0
    while True:
        success, img = cap.read()

        # skip few frames to be more realtime-like
        count += 5
        cap.set(cv2.CAP_PROP_POS_FRAMES, count)
        if not success:
            break
        
        img = cv2.imencode('.jpg', img)[1].tobytes()
        publisher.send_multipart([id.to_bytes(2, 'big'), img])
        sleep(0.1) # delay to avoid frames skipping

    publisher.close()
    context.term()


def run():
    """generate videosource processes"""

    processes = []
    for id, source in enumerate(config['sources']):
        processes.append(Process(target=start_source, args=(id, source)))
        print('inited process')
    for process in processes:
        process.start()
