import time
# import threading
# import os
from comms import intranode, internode

class controller:
    def __init__(self):
        self.is_running = True
        self.commands = {"pconfig": self.config,
                        "psubmit": self.submit} #all commands
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
        elif option == "none":
            None #set up worker configuration
        else:
            print(f'Invalid argument in pconfig: {option}')

    def submit(self):
        self.comm.write("next")
        files = []
        arg = self.comm.read()
        while arg != "done":
            files.append(arg)
            arg = self.comm.read()
        
        comm = internode(host="192.168.0.32")
        comm.start()
        comm.connect()
        comm.write("job")
        comm.read()
        comm.write(files[0])
        comm.read()

        for i in files:
            print(i)


        

if __name__ == "__main__":
    m = controller()
    m.start()