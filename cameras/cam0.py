import zmq
import cv2


def main():
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://0.0.0.0:5557")
    # publisher.setsockopt(zmq.SNDHWM, 1)

    cap = cv2.VideoCapture('videos/forklift1.mp4')
    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.imencode('.jpg', img)[1].tobytes()
        publisher.send_multipart([b"0", img])
        # print(f'[CAM2]: sent frame')

    # We never get here but clean up anyhow
    publisher.close()
    context.term()


if __name__ == "__main__":
    main()