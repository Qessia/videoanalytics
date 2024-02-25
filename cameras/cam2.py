import zmq
import cv2


def main():
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://*:5560")

    cap = cv2.VideoCapture('videos/oilstation.mp4')

    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.imencode('.jpg', img)[1].tobytes()
        publisher.send_multipart([b"CAM2", img])
        print(f'[CAM2]: sent frame')

    # We never get here but clean up anyhow
    publisher.close()
    context.term()


if __name__ == "__main__":
    main()