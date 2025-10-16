from comms import internode

class worker:
    def __init__(self):
        # self.node_name = "NAMELESS NODE"
        self.is_running = True
        self.status = "UNKOWN"
        self.commands = {"config":self.config,
                        "job": self.job}
        self.controller_ip = ""
        # self.port = 25732
        
    def start(self):
        self.comm = internode(server=True)
        self.comm.start()
        self.comm.bind()
        self.comm.listen()
        while True:
            self.comm.accept()
            cmd = self.comm.read()
            if cmd in self.commands:
                self.commands[cmd]()
            self.comm.close()
        self.comm.kill()

    def config(self):
        self.comm.write("next")
        self.controller_ip = self.comm.read()
        print("configured")
        self.comm.write("UP")
        

    def job(self):
        self.comm.write("next")
        file = self.comm.read()
        self.comm.write("thanks")
        print(file)

if __name__ == "__main__":
    w = worker()
    w.start()