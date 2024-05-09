import zmq
from config import config


def main():
    # Prepare our context and router
    context = zmq.Context()

    subscriber = context.socket(zmq.SUB)
    for s in config['sources']:
        subscriber.connect(s['port'])
    subscriber.setsockopt(zmq.SUBSCRIBE, b"")

    workers = []
    for w in config['workers']:
        worker = context.socket(zmq.PUSH)
        worker.connect(w)
        workers.append(worker)

    while True:
        [address, contents] = subscriber.recv_multipart()
        workers[int.from_bytes(address)].send_multipart([address, contents])
    
    # We never get here but clean up anyhow
    subscriber.close()
    context.term()