import zmq
import numpy as np
import cv2


def main():

    # Prepare our context and router
    context = zmq.Context()

    # subs = [context.socket(zmq.SUB)]
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5559")
    subscriber.connect("tcp://localhost:5560")
    subscriber.connect("tcp://localhost:5558")
    subscriber.connect("tcp://localhost:5557")
    # subscriber.setsockopt(zmq.RCVHWM, 1)
    subscriber.setsockopt(zmq.SUBSCRIBE, b"")

    worker0 = context.socket(zmq.PUSH)
    worker0.connect("tcp://127.0.0.1:5561")

    worker1 = context.socket(zmq.PUSH)
    worker1.connect("tcp://127.0.0.1:5563")

    balance = 0
    while True:
        [address, contents] = subscriber.recv_multipart()

        if balance % 2 == 0:
            worker0.send_multipart([address, contents])
        else:
            worker1.send_multipart([address, contents])
    

    # We never get here but clean up anyhow
    subscriber.close()
    context.term()


if __name__ == "__main__":
    main()