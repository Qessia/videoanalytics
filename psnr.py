import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio
import matplotlib.pyplot as plt
import argparse
import sys


def get_meanframe(normal_videopath, meanframe_path):
    """Creates meanframe of video

    Args:
        normal_videopath (str): path of "normal" video
        meanframe_path (str): path to save meanframe to
    """
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

def plot_psnr(meanframe_path, video_path):
    """Plot PSNR plot (X axis - frames, Y axis - PSNR in dB)

    Args:
        meanframe_path (str): destination of meanframe in .jpg format
        video_path (str): destination of video with emergency situation
    """
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


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('videopath', type=str, help='path of "normal" video')

    try:
        args = parser.parse_args()
        get_meanframe(args.videopath, args.videopath[:-4] + '_meanframe.jpg')
    except:
        parser.print_help()
        sys.exit(0)


if __name__ == '__main__':
    main()
