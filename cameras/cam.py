import zmq
import cv2
from typing import List
from multiprocessing import Process


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
        print(id)
    publisher.close()
    context.term()


def run(sources: List[dict]):
    processes = []
    for id, source in enumerate(sources):
        processes.append(Process(target=start_source, args=(id, source)))
        print('inited process')
    for process in processes:
        process.start()


def main():
    sources = [
        {
            'port': 'tcp://0.0.0.0:5557',
            'path': '../videos/forklift1.mp4',
        },
        {
            'port': 'tcp://0.0.0.0:5559',
            'path': '../videos/forklift2.mp4',
        },
        {
            'port': 'tcp://0.0.0.0:5560',
            'path': '../videos/oilstation.mp4',
        },
        {
            'port': 'tcp://0.0.0.0:5558',
            'path': '../videos/alumin.mp4',
        }
    ]
    run(sources)


if __name__ == "__main__":
    main()
