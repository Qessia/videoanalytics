import zmq
import numpy as np
import cv2


def main():

    # Prepare our context and router
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5559")
    subscriber.connect("tcp://localhost:5560")
    subscriber.connect("tcp://localhost:5558")
    subscriber.connect("tcp://localhost:5557")
    subscriber.setsockopt(zmq.SNDHWM, 4)

    router = context.socket(zmq.ROUTER)
    router.bind("tcp://0.0.0.0:5561")

    rr_step = 0
    vid_step = 0
    while True:
        ident = b'W0'
        address = [b'0', b'1', b'2', b'3'][vid_step]
        ident = [b'W0', b'W1'][rr_step]

        subscriber.setsockopt(zmq.SUBSCRIBE, address)
        [address, contents] = subscriber.recv_multipart()
        router.send_multipart([ident, address, contents])

        rr_step = (rr_step + 1) % 2
        vid_step = (vid_step + 1) % 4
    

    # We never get here but clean up anyhow
    subscriber.close()
    context.term()


if __name__ == "__main__":
    main()