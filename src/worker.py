import socket

class worker:
    def __init__(self):
        self.node_name = None
        self.running = True
        self.status = ""
        self.commands = 

    def workerloop(self):
        while self.running:
            cmd = self.listen()
            if cmd in self.commands:
                self.commands[cmd]()
            else:
                print("Unrecognised command")
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


# HOST = ''                 # Symbolic name meaning all available interfaces
# PORT = 50007              # Arbitrary non-privileged port

# def listen():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind((HOST, PORT))
#         s.listen(1)
#         conn, addr = s.accept()
#         with conn:
#             print('Connected by', addr)
#             while True:
#                 data = conn.recv(1024)
#                 if not data: break
#                 print("Message:", data.decode())
        
if __name__ == "__main__":
    w = worker()
    while True:
        w.listen()
