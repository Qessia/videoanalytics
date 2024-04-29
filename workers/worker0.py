import zmq
import numpy as np
import cv2
import torch
from ultralytics import YOLO


def main():

    if torch.cuda.is_available():
        torch.cuda.set_device(0)

    model = YOLO('models/forklift_8s.pt')  # pretrained YOLOv8n model
    # Prepare our context and publisher
    context = zmq.Context()
    puller = context.socket(zmq.PULL)
    puller.bind("tcp://127.0.0.1:5561")

    pusher = context.socket(zmq.PUSH)
    pusher.connect("tcp://127.0.0.1:5562")

    while True:
        [address, contents] = puller.recv_multipart()

        encoded_frame = np.frombuffer(contents, dtype=np.uint8)
        frame = cv2.imdecode(encoded_frame, cv2.IMREAD_COLOR)

        result = model(frame)[0]  # return a list of Results objects
        result = result.tojson()

        data = [address, contents, result.encode()]
        pusher.send_multipart(data)
        print(data[0])
    

    # We never get here but clean up anyhow
    pusher.close()
    context.term()


if __name__ == "__main__":
    main()