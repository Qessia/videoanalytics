import zmq
import numpy as np
import cv2
import torch
from ultralytics import YOLO


def main():

    if torch.cuda.is_available():
        torch.cuda.set_device(0)

    model = YOLO('models/yolov8n.pt')  # pretrained YOLOv8n model
    # Prepare our context and publisher
    context = zmq.Context()
    dealer = context.socket(zmq.DEALER)
    dealer.setsockopt(zmq.IDENTITY, b'W0')
    dealer.connect("tcp://localhost:5561")

    pusher = context.socket(zmq.PUSH)
    pusher.connect("tcp://localhost:5562")

    while True:
        [address, contents] = dealer.recv_multipart()

        encoded_frame = np.frombuffer(contents, dtype=np.uint8)
        frame = cv2.imdecode(encoded_frame, cv2.IMREAD_COLOR)

        result = model(frame)[0]  # return a list of Results objects
        result = result.tojson()

        pusher.send_multipart([address, contents, result.encode()])
    

    # We never get here but clean up anyhow
    dealer.close()
    context.term()


if __name__ == "__main__":
    main()