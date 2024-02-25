import zmq
import numpy as np
import cv2


def main():

    # Prepare our context and publisher
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5559")
    subscriber.connect("tcp://localhost:5560")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"")

    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://0.0.0.0:5561")

    while True:
        [address, contents] = subscriber.recv_multipart()
        publisher.send_multipart([address, contents])
    

    # We never get here but clean up anyhow
    subscriber.close()
    context.term()


if __name__ == "__main__":
    main()