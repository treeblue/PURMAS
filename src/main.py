import time
import threading
import os
import socket

class controller:
    def __init__(self):
        self.is_running = False
        self.is_paused = False
        self.cycle = 1. #sleep time between loop updates
        self.commands = {"stop": self.stop,
                        "stop all": self.stop_all,
                        "pause": self.pause,
                        "help": self.help,
                        "config": self.read_config,
                        "send": self.send,
                        "status": self.show_status} #all user commands
        # self.worker_commands = {"print":}
        self.nodes = {}
        self.status = {}
        self.jobs = {}
        self.send_port = 25732
        self.listen_port = 25732

    def mainloop(self):
        while self.is_running:
            if not self.is_paused:
                # self.listen()
                None
            else:
                time.sleep(self.cycle)

    def take_inputs(self):
        while self.is_running:
            cmd = input("> ")
            if cmd in self.commands:
                self.commands[cmd]()
            else:
                print("Unrecognised command")
            time.sleep(self.cycle)

    def start(self):
        self.read_config()
        self.is_running = True
        ctl = threading.Thread(target=self.mainloop)
        ctl.daemon = True
        ctl.start()
        print("[controller] Scheduler is running")
        self.take_inputs()
        ctl.join()

    def stop(self):
        print("[controller] Scheduler is stopping")
        self.is_running = False
    
    def stop_all(self):
        print("[controller] Stopping workers")
        for node_name in self.nodes:
            self.send(node_name,"stop")
        self.stop()

    def pause(self):
        if self.is_paused:
            print("[controller] Resuming daemon")
            self.is_paused = False
        else:
            self.is_paused = True
            time.sleep(self.cycle)
            print("[controller] Pausing daemon")

    def help(self):
        print("\nAvailable user commands:")
        for cmd in self.commands:
            print(f" - {cmd}")
        print("")

    def read_config(self):
        if self.is_running:
            if not self.is_paused:
                self.pause()
        
        print("[controller] Reading config file...")
        try:
            open(__file__.replace("main.py","config.txt"), 'r')
        except:
            raise Exception("[controller] Unable to read config file")
        config_file = open(__file__.replace("main.py","config.txt"), 'r')
        
        for line in config_file:
            if line[:12] == "Controller: ":
                self.controller_ip = line[12:].strip('\n')
                break

        print("[controller] Replacing node information files...")
        node_dir = __file__.replace("/src/main.py","/Nodes")
        try:
            os.listdir(node_dir)
        except:
            raise Warning("[controller] Could not update the /Nodes directory")

        self.nodes = {}
        for file in os.listdir(node_dir):
            os.remove(f"{node_dir}/{file}")
        for line in config_file:
            if line[:6] == "Node: ":
                node_info = line.split()
                try:
                    node_name = node_info[1]
                    node_ip = node_info[2]
                    with open(f"{node_dir}/{node_name}.txt",'w') as node_file:
                        node_file.write(f"ip address: {node_ip}\n")
                    self.nodes[node_name] = node_ip
                except:
                    print(f"[controller] Incorrect config file syntax:\n{line}Should be in the following format:\nNode: [node_name] [node_ip]")
        
        print("[controller] Checking nodes...")
        self.status = {}
        for node_name in self.nodes:
            try:
                #tell worker to configure
                self.send(node_name,"config")
                time.sleep(2*self.cycle)
                #send: controller ip
                self.send(node_name,self.controller_ip)
                #send: node name
                self.send(node_name,node_name)
                print(self.listen(10.))
                self.status[node_name] = self.listen(10.)
            except:
                self.status[node_name] = "DOWN"

        print("[controller] Configured")
        config_file.close()
        
        if self.is_running:
            self.pause()

    def send(self, listener:str , message:str):
        time.sleep(self.cycle)
        HOST = self.nodes[listener]
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

    def listen(self, timeout:float=10.)->str:
        time.sleep(self.cycle)
        HOST = ''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST,self.listen_port))
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

    def get_status(self):
        for node_name in self.nodes:
            try:
                self.send(node_name,"status")
                self.status[node_name] = self.listen()
            except:
                continue

    def show_status(self):
        self.get_status()
        print("NAME\t | STATUS")
        for node_name in self.nodes:
            print(f"{node_name}\t | {self.status[node_name]}")
            
            
            

if __name__ == "__main__":
    m = controller()
    m.start()
