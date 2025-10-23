from comms import internode
import subprocess
import os

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
        while self.is_running:
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
        
    def job(self): #THESE DONT WORK PROPERLY UNLESS RUN FROM PURMAS FOLDER!!!
        self.comm.write("next")
        file = self.comm.read()
        self.comm.write("next")
        JID = self.comm.read()
        self.comm.write("thanks")
        print(f"Running job {JID}: {file}")

        process = subprocess.Popen(["bash", file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        with open(f"Jobs/{JID}stdout.txt", "w") as file:
            file.write(stdout.decode())
        with open(f"Jobs/{JID}stderr.txt", "w") as file:
            file.write(stderr.decode())

        print(f"Job {JID} finished")
        

if __name__ == "__main__":
    w = worker()
    w.start()