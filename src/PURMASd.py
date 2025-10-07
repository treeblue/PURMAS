import time
# import threading
# import os
from comms import intranode

class controller:
    def __init__(self):
        self.is_running = True
        self.commands = {"pconfig": self.config} #all commands
        self.nodes = {} #node name and node ip
        self.status = {} #node name and node status
        self.jobs = {}

    def start(self):
        self.comm = intranode(server=True)
        self.comm.start()
        self.comm.bind()
        self.comm.listen()
        while self.is_running:
            self.comm.accept()
            cmd = self.comm.read()
            if cmd in self.commands:
                self.commands[cmd]()
            self.comm.close()
        self.comm.kill()

    def config(self):
        self.comm.write("next")
        option = self.comm.read()
        if option == "stop":
            self.is_running = False
        else:
            print(f'Invalid argument in pconfig: {option}')



if __name__ == "__main__":
    m = controller()
    m.start()