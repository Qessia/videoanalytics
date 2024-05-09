from multiprocessing import Process
import gui
import broker
from cameras import cam
from workers import worker


if __name__ == "__main__":
    
    broker_process = Process(target=broker.main)
    worker_process = Process(target=worker.main)
    gui_process = Process(target=gui.main)

    worker_process.start()
    broker_process.start()
    cam.run() # start camera Processes
    gui_process.start()