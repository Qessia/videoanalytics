import zmq
import cv2
from typing import List
from multiprocessing import Process
import json

def start_source(id, source: dict):
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(source['port'])
    cap = cv2.VideoCapture(source['path'])
    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.imencode('.jpg', img)[1].tobytes()
        publisher.send_multipart([id.to_bytes(2, 'big'), img])

    publisher.close()
    context.term()


def run(sources: List[dict]):
    processes = []
    for id, source in enumerate(sources):
        processes.append(Process(target=start_source, args=(id, source)))
        print('inited process')
    for process in processes:
        process.start()


def main(config):
    run(config['sources'])


if __name__ == "__main__":
    main()
