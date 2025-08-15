import time
import socket

class worker:
    def __init__(self):
        self.node_name = "NAMELESS NODE"
        self.is_running = True
        self.is_paused = False
        self.status = "UNKOWN"
        self.commands = {"stop": self.stop,
                        "config": self.configure}
        self.cycle = 1.
        self.controller_ip = ""

    def workerloop(self):
        while self.is_running:
            if not self.is_paused:
                cmd = self.listen()
                if cmd in self.commands:
                    self.commands[cmd]()
            time.sleep(self.cycle)

    def listen(self):
        time.sleep(self.cycle)
        HOST = ''
        PORT = 50007
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data: break
                    return data.decode()

    def send(self, message:str):
        time.sleep(self.cycle)
        HOST = self.controller_ip
        PORT = 50007
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(message.encode())

    def stop(self):
        print(f"[{self.node_name}] worker is stopping")
        self.is_running = False

    def configure(self):
        self.is_paused = True
        time.sleep(self.cycle)
        print("configuring...")
        #expect controller to send information in specific order:
        #controller ip
        #worker node name
        self.controller_ip = self.listen()
        self.node_name = self.listen()
        time.sleep(self.cycle)
        print(f"[{self.node_name}] Configured")
        self.send(f"[{self.node_name}] Configured")
        self.send(self.status)
        self.is_paused = False


if __name__ == "__main__":
    w = worker()
    w.workerloop()
