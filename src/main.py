import time
import threading
import os

class master:
    def __init__(self):
        self.is_running = False
        self.is_paused = False
        self.cycle = 1. #sleep time between loop updates
        self.commands = {"stop": self.stop,
                        "pause": self.pause,
                        "help": self.help,
                        "config": self.read_config} #all user commands
        self.jobs = {}

    def mainloop(self):
        while self.is_running:
            if not self.is_paused:
                None
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
        self.is_running = True
        ctl = threading.Thread(target=self.mainloop)
        ctl.daemon = True
        ctl.start()
        print("[controller] Scheduler is running")
        self.take_inputs()
        ctl.join()

    def stop(self):
        print("[controller] scheduler is stopping")
        self.is_running = False

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
        if not self.is_paused:
            self.pause()
        
        try:
            open(__file__.replace("main.py","config.txt"), 'r')
        except:
            raise Exception("[controller] Unable to read config file")
        config_file = open(__file__.replace("main.py","config.txt"), 'r')

        node_dir = __file__.replace("/src/main.py","/Nodes")
        try:
            os.listdir(node_dir)
        except:
            raise Warning("[controller] Could not update the /Nodes directory")
        
        print("[controller] Replacing Node information files...")
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
                    raise Warning(f"[controller] Incorrect config file syntax:\n{line}Should be in the following format:\nNode: [node_name] [node_ip]")
        print(self.nodes)

        print("[controller] Configured")
        config_file.close()
        
            
        self.pause()
        

m = master()
m.start()
