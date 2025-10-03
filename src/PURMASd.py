import time
# import threading
# import os
from comms import intranode

class controller:
    def __init__(self):
        self.is_running = True
        self.nodes = {} #node name and node ip
        self.status = {} #node name and node status
        self.jobs = {}

    def start(self):
        comm = intranode()
        comm.start()
        comm.bind()
        comm.listen()
        while self.is_running:
            comm.accept()
            cmd = comm.read()
            print(cmd)
            self.is_running = False
            comm.close()
            
if __name__ == "__main__":
    m = controller()
    m.start()