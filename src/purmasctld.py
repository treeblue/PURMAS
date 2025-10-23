import time
import threading
import os
from comms import intranode, internode

class controller:
    def __init__(self):
        self.is_running = False
        self.commands = {"pconfig": self.config,
                        "psubmit": self.submit,
                        "pinfo": self.info} #all commands
        self.nodes = {} #node name and node ip
        self.status = {} #node name and node status
        self.jobs = {} #job id and job file
        self.pending = {} #job id and job file
        self.job_no = 1

    # scheduler controls

    def start(self):
        self.is_running = True
        #start scheduler
        ctl = threading.Thread(target=self.scheduler)
        ctl.daemon = True
        ctl.start()

        #start unix port and listen
        self.comm = intranode(server=True)
        self.comm.start()
        self.comm.bind()
        self.comm.listen()
        print("[controller] UNIX port active and listening")
        while self.is_running:
            self.comm.accept()
            cmd = self.comm.read()
            if cmd in self.commands:
                self.commands[cmd]()
            self.comm.close()
        self.comm.kill()

    def scheduler(self):
        while self.is_running:
            time.sleep(60.) #change to a varied timer
            if len(self.jobs) == 0:
                print("[controller] Job list empty...")
            elif len(self.nodes) == 0:
                print("[controller] No worker nodes! Try updating the config file and running pconfig")
            else:
                self.assign_job()
                print(f"[controller] {len(self.jobs)} job(s) scheduled")

            if len(self.pending) > 0:
                self.job_cleanup()

    def assign_job(self):
        #choose node better
        host = None
        for node in self.nodes:
            if self.status[node] == "UP":
                host = node
                break

        if host == None:
            return None

        #choose job better
        #check job is valid
        JID = None
        for job in self.jobs:
            JID = job
            break

        comm = internode(host=self.nodes[host])
        comm.start()
        comm.connect()
        comm.write("job")
        comm.read()
        comm.write(self.jobs[JID])
        comm.read()
        comm.write(f"{JID}")
        comm.read()

        self.status[host] = "BUSY"
        self.pending[JID] = [self.jobs[JID],host]
        del self.jobs[JID]

    def job_cleanup(self): #THIS DOESNT WORK PROPERLY UNLESS RUN FROM PURMAS FOLDER!!!
        #just checks if files exists and resets worker status
        done = []
        for JID in self.pending:
            try:
                with open(f"Jobs/{JID}stdout.txt", 'r') as stdout:
                    None
                self.status[self.pending[JID][1]] = "UP"
                done.append(JID)
            except:
                None

        for JID in done:
            del self.pending[JID]


    #admin controls

    def config(self):
        self.comm.write("next")
        option = self.comm.read()
        if option == "stop":
            self.is_running = False
        elif option == "none":
            print("[controller] Reading config file...")
            try:
                open(__file__.replace("purmasctld.py","config.txt"), 'r')
            except:
                raise Exception("[controller] Unable to read config file")
            config_file = open(__file__.replace("purmasctld.py","config.txt"), 'r')
            
            for line in config_file:
                if line[:12] == "Controller: ":
                    self.controller_ip = line[12:].strip('\n')
                    break

            print("[controller] Replacing node information files...")
            node_dir = __file__.replace("/src/purmasctld.py","/Nodes")
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
                    comm = internode(host=self.nodes[node_name])
                    comm.start()
                    comm.connect()
                    #tell worker to configure
                    comm.write("config")
                    comm.read()
                    #send: controller ip
                    comm.write(self.controller_ip)
                    #set node status
                    self.status[node_name] = comm.read()
                except:
                    self.status[node_name] = "DOWN"

            print("[controller] Configured")
            config_file.close()
        else:
            print(f'Invalid argument in pconfig: {option}')

    #user controls

    def submit(self):
        self.comm.write("next")
        files = []
        arg = self.comm.read()
        while arg != "done":
            files.append(arg)
            arg = self.comm.read()
        
        for file in files:
            self.jobs[self.job_no] = file
            print(f"[controller] Job {self.job_no} submitted")
            self.job_no += 1

        # comm = internode(host="192.168.0.32")
        # comm.start()
        # comm.connect()
        # comm.write("job")
        # comm.read()
        # comm.write(files[0])
        # comm.read()

    def info(self): #wont show jobs in pending
        self.comm.write("next")
        mode = self.comm.read()

        if mode == "all" or mode == "nodes":
            for node in self.nodes:
                # print(f'{node}\t| {self.nodes[node]}\t| {self.status[node]}')
                self.comm.write(f'{node}\t| {self.nodes[node]}\t| {self.status[node]}')
                self.comm.read()
            self.comm.write("done")
            self.comm.read()

        if mode == "all" or mode == "jobs":
            for job in self.jobs:
                # print(f'{job}\t| {self.jobs[job]}')
                self.comm.write(f'{job}\t| {self.jobs[job]}')
                self.comm.read()
            self.comm.write("done")
            self.comm.read()
        

if __name__ == "__main__":
    m = controller()
    m.start()