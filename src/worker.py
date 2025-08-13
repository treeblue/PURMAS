import time
import socket

class worker:
    def __init__(self):
        self.node_name = "NAMELESS NODE"
        self.is_running = True
        self.status = ""
        self.commands = {"stop": self.stop}
        self.cycle = 1.

    def workerloop(self):
        while self.is_running:
            cmd = self.listen()
            if cmd in self.commands:
                self.commands[cmd]()
            time.sleep(self.cycle)

    def listen(self):
        HOST = ''
        PORT = 50007
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data: break
                    return data.decode()

    def stop(self):
        print(f"[{self.node_name}] worker is stopping")
        self.is_running = False

    # def handshake(self):


if __name__ == "__main__":
    w = worker()
    w.workerloop()
