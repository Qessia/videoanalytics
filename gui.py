import zmq
import numpy as np
import cv2
import json


class GUI:
    def __init__(self):
        self.width = 1920
        self.height = 1080
        self._canvas = np.ones((self.height, self.width, 3), dtype=np.uint8) * 40  # gray canvas
        self.grid = (2, 2) # (WIDTH, HEIGHT)
        self.cells = np.zeros((self.grid[0]*self.grid[1], self.height, self.width, 3))

    @property
    def canvas(self):
        return self._canvas
    
    def update_cell(self, n: int, img):
        idx = (n // self.grid[0], n % self.grid[0])
        w_pix = int(self.width / self.grid[0])
        h_pix = int(self.height / self.grid[1])

        w_start = idx[0] * w_pix
        h_start = idx[1] * h_pix

        img = cv2.resize(img, (w_pix, h_pix), interpolation=cv2.INTER_CUBIC)
        self._canvas[h_start:h_start+h_pix, w_start:w_start+w_pix] = img


def main():

    # Prepare our context and publisher
    context = zmq.Context()
    puller = context.socket(zmq.PULL)
    puller.bind("tcp://0.0.0.0:5562")
    print('GUI')
    gui = GUI()

    while True:
        addr, img, dets = puller.recv_multipart()
        print(addr, dets)
        addr = int.from_bytes(addr)

        img = cv2.imdecode(np.frombuffer(img, dtype=np.uint8), cv2.IMREAD_COLOR)
        dets = json.loads(dets.decode())
        
        for d in dets:
            x1 = int(d['box']['x1'])
            y1 = int(d['box']['y1'])
            x2 = int(d['box']['x2'])
            y2 = int(d['box']['y2'])
            img = cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)
            name = d['name']
            img = cv2.putText(img, name, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        gui.update_cell(addr, img)
        
        cv2.imshow('Image', gui.canvas)
        if cv2.waitKey(10) & 0xFF == 27:
            cv2.destroyAllWindows()
            break
    

    # We never get here but clean up anyhow
    puller.close()
    context.term()


if __name__ == "__main__":
    main()