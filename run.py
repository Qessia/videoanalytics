from pathlib import Path
from multiprocessing import Process

from cameras import cam
import broker
from workers import (worker0, worker1)
import gui
import json


if __name__ == "__main__":
    with open('./config.json', 'r') as f:
        config = json.load(f)
    
    broker_process = Process(target=broker.main)
    worker0_process = Process(target=worker0.main)
    worker1_process = Process(target=worker1.main)
    gui_process = Process(target=gui.main)

    worker0_process.start()
    worker1_process.start()
    broker_process.start()

    cam.main(config)
    gui_process.start()