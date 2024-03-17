import time
import zmq
import cv2


def main():
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://0.0.0.0:5559")

    cap = cv2.VideoCapture('videos/forklift2.mp4')

    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.imencode('.jpg', img)[1].tobytes()
        publisher.send_multipart([b"1", img])
        # print(f'[CAM1]: sent frame')

    # We never get here but clean up anyhow
    publisher.close()
    context.term()


if __name__ == "__main__":
    main()