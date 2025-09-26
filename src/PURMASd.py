import time
import threading
import os
import socket

class controller:
    def __init__(self):
        self.is_paused = False
        self.nodes = {} #node name and node ip
        self.status = {} #node name and node status
        self.jobs = {}

    def start(self):
        s = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
        s.bind("/tmp/PURMAS_input.sock")
        s.listen(5)
        while True:
            conn, _ = s.accept()
            data = conn.recv(1024)
            cmd = data.decode()
            #do things
            conn.send(b"PURMAS_done")
            conn.close()
            
if __name__ == "__main__":
    m = controller()
    m.start()