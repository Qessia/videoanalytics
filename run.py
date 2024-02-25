from pathlib import Path
from multiprocessing import Process

from cameras import (cam1, cam2)
import broker
import worker1
import gui

if __name__ == "__main__":
    cam1_process = Process(target=cam1.main)
    cam2_process = Process(target=cam2.main)
    broker_process = Process(target=broker.main)
    worker1_process = Process(target=worker1.main)
    gui_process = Process(target=gui.main)

    gui_process.start()
    worker1_process.start()
    broker_process.start()
    cam1_process.start()
    cam2_process.start()
