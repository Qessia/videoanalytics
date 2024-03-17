from pathlib import Path
from multiprocessing import Process

from cameras import (cam0, cam1, cam2, cam3)
import broker
from workers import (worker0, worker1)
import gui

if __name__ == "__main__":
    cam0_process = Process(target=cam0.main)
    cam1_process = Process(target=cam1.main)
    cam2_process = Process(target=cam2.main)
    cam3_process = Process(target=cam3.main)
    
    broker_process = Process(target=broker.main)
    worker0_process = Process(target=worker0.main)
    worker1_process = Process(target=worker1.main)
    gui_process = Process(target=gui.main)

    gui_process.start()
    worker0_process.start()
    worker1_process.start()
    broker_process.start()

    cam0_process.start()
    cam1_process.start()
    cam2_process.start()
    cam3_process.start()