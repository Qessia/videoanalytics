from pathlib import Path
from multiprocessing import Process

import cameras
import broker as broker

if __name__ == "__main__":
    reader_process = Process(target=cameras.cam1.main)
    cam2_process = Process(target=cameras.cam2.main)
    broker_process = Process(target=broker.main)
    
    broker_process.start()
    reader_process.start()
    cam2_process.start()
