import time
import socket

class worker:
    def __init__(self):
        self.node_name = "NAMELESS NODE"
        self.is_running = True
        self.is_paused = False
        self.status = "UNKOWN"
        self.commands = {"stop": self.stop,
                        "config": self.configure,
                        "status": self.send_status}
        self.cycle = 1.
        self.controller_ip = ""
        self.send_port = 25732
        self.listen_port = 25732

    def workerloop(self):
        while self.is_running:
            if not self.is_paused:
                self.update_status()
                cmd = self.listen(10.)
                if cmd in self.commands:
                    self.commands[cmd]()
            else:
                time.sleep(self.cycle)

    def listen(self, timeout:float=10.)->str:
        time.sleep(self.cycle)
        HOST = ''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, self.listen_port))
            s.listen()
            s.settimeout(timeout)
            try:
                conn, addr = s.accept()
                with conn:
                    while True:
                        data = conn.recv(1024)
                        if not data: break
                        return data.decode()
            except socket.timeout:
                None
            return ""

    def send(self, message:str):
        time.sleep(self.cycle)
        HOST = self.controller_ip
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, self.send_port))
                s.sendall(message.encode())
            except:
                time.sleep(self.cycle)
                try:
                    s.connect((HOST, self.send_port))
                    s.sendall(message.encode())
                except:
                    None

    def stop(self):
        print(f"[{self.node_name}] Worker is stopping")
        self.is_running = False

    def configure(self):
        self.is_paused = True
        time.sleep(self.cycle)
        print("Configuring...")
        #expect controller to send and receive information in specific order:
        #listen for: controller ip
        self.controller_ip = self.listen()
        #listen for: worker node name
        self.node_name = self.listen()
        #send: message
        time.sleep(self.cycle)
        print(f"[{self.node_name}] Configured")
        self.send(f"[{self.node_name}] Configured")
        #send: status
        self.send(self.status)

        self.is_paused = False

    def update_status(self):
        if not self.is_paused:
            self.status = "UP"
        elif self.is_paused:
            self.status = "PAUSED"
        else:
            self.status = "UNKOWN"
    
    def send_status(self):
        time.sleep(self.cycle)
        self.send(self.status)
        time.sleep(self.cycle)

if __name__ == "__main__":
    w = worker()
    w.workerloop()
