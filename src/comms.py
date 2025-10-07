import socket
import os

class intranode:
    def __init__(self, sock_loc:str = "/tmp/PURMAS_input.sock", server:bool = False):
        self.sock_loc = sock_loc
        self.server = server
        # self.end_msg = b"end_comm"
    
    #general
    def start(self):
        if self.server and os.path.exists(self.sock_loc):
            os.remove(self.sock_loc)  # remove old socket file
        self.sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)

    #server
    def bind(self):
        self.sock.bind(self.sock_loc)

    def listen(self, n:int=1):
        self.sock.listen(n)

    def accept(self):
        self.conn, _ = self.sock.accept()

    #client
    def connect(self):
        self.sock.connect(self.sock_loc)

    #communication
    def write(self,message:str):
        if self.server:
            self.conn.sendall(message.encode())
        else:
            self.sock.sendall(message.encode())

    def read(self)->str:
        if self.server:
            data = self.conn.recv(1024).decode()
            return data
        else:
            data = self.sock.recv(1024).decode()
            return data

    def close(self):
        if self.server:
            self.conn.close()

    def kill(self):
        self.sock.close()


class internode:
    def __init__(self, host:str = '', server:bool = False):
        self.sock_loc = host
        self.server = server
        # self.port = 25732

    #general
    def start(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    #server
    def bind(self,port:int=25732):
        self.sock.bind((self.sock_loc,port))

    def listen(self, n:int=1):
        self.sock.listen(n)

    def accept(self)->str:
        self.conn, _ = self.sock.accept()

    #client
    def connect(self,port:int=25732):
        self.sock.connect((self.sock_loc,port))

    #communication
    def write(self,message:str):
        if self.server:
            self.conn.sendall(message.encode())
        else:
            self.sock.sendall(message.encode())

    def read(self)->str:
        if self.server:
            data = self.conn.recv(1024).decode()
            return data
        else:
            data = self.sock.recv(1024).decode()
            return data

    def close(self):
        if self.server:
            self.conn.close() 

    def kill(self):
        self.sock.close()

#intra example
if False:
    #server
    comm = intranode(server=True)
    comm.start()
    comm.bind()
    comm.listen()
    while True:
        comm.accept()
        message = comm.read()
        #do thing with message
        comm.close()
    comm.kill()

    #client
    comm = intranode()
    comm.start()
    comm.connect()
    comm.write("hello world")

#inter example??