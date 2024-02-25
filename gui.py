import zmq
import numpy as np
import cv2
import json


def main():

    # Prepare our context and publisher
    context = zmq.Context()
    puller = context.socket(zmq.PULL)
    puller.bind("tcp://*:5562")

    while True:
        addr, img, dets = puller.recv_multipart()

        addr = addr.decode()
        img = cv2.imdecode(np.frombuffer(img, dtype=np.uint8), cv2.IMREAD_COLOR)
        dets = json.loads(dets.decode())

        for d in dets:
            pass # TODO

        cv2.imshow('Image', frame)
        cv2.waitKey(10)
        if cv2.waitKey(10) & 0xFF == 27:
            cv2.destroyAllWindows()
            break
    

    # We never get here but clean up anyhow
    puller.close()
    context.term()


if __name__ == "__main__":
    main()