import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio
import matplotlib.pyplot as plt


def get_meanframe(normal_videopath, meanframe_path):
    before = cv2.VideoCapture(normal_videopath)
    success, img = before.read()
    frames = 0
    avg = np.zeros((720,1280,3), dtype=np.float64)

    while True:
        success, img = before.read()
        if not success or img is None:
            break
        avg = np.add(avg, img)
        frames += 1

    before.release()
    avg = np.divide(avg, frames).astype(np.uint8)
    
    cv2.imwrite(meanframe_path, avg)


def main():
    meanframe_path = './videos/alumin_meanframe.jpg'
    video_path = './videos/alumin.mp4'

    meanframe = cv2.imread(meanframe_path)

    PSNR = []
    before = cv2.VideoCapture(video_path)
    success, img = before.read()

    while True:
        success, img = before.read()
        if not success or img is None:
            break
        PSNR.append(peak_signal_noise_ratio(meanframe, img))
    before.release()

    plt.plot(PSNR)
    plt.show()


if __name__ == '__main__':
    main()
