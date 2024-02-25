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

    while True:
        [address, contents] = subscriber.recv_multipart()

        encoded_frame = np.frombuffer(contents, dtype=np.uint8)
        frame = cv2.imdecode(encoded_frame, cv2.IMREAD_COLOR)

        cv2.imshow('Image', frame)
        cv2.waitKey(10)
        if cv2.waitKey(10) & 0xFF == 27:
            cv2.destroyAllWindows()
            break
    

    # We never get here but clean up anyhow
    subscriber.close()
    context.term()


if __name__ == "__main__":
    main()