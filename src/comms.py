import socket

class intranode:
    def __init__(self, sock_loc:str = "/tmp/PURMAS_input.sock"):
        self.sock_loc = sock_loc
        # self.end_msg = b"end_comm"
    
    #general
    def start(self):
        self.sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)

    #server
    def bind(self):
        self.sock.bind(self.sock_loc)

    def listen(self, n:int=1):
        self.sock.listen(n)

    def accept(self)->str:
        self.conn, _ = self.sock.accept()

    #client
    def connect(self):
        self.sock.connect(self.sock_loc)

    #communication
    def write(self,message:str):
        self.conn.sendall(message.encode())

    def read(self)->str:
        data = self.conn.recv(1024).decode()
        return data.decode()

    def close(self):
        self.conn.close()


class internode:
    def __init__(self):
        self.socket = ""

if __name__ == "__main__":
    intra = intranode()