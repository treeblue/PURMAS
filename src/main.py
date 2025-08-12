import time
import threading

class master:
    def __init__(self):
        self.is_running = False
        self.is_paused = False
        self.cycle = 1. #sleep time between loop updates
        self.commands = {"stop": self.stop,
                        "pause": self.pause,
                        "help": self.help} #all user commands
        self.nodes = {}
        self.jobs = {}

    def mainloop(self):
        if self.is_running: print("[controller] scheduler is running")
        i = 0
        while self.is_running:
            if not self.is_paused:
                None
            time.sleep(self.cycle)
            i += 1
            if i > 10:
                self.is_running = False

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
        self.take_inputs()
        ctl.join()

    def stop(self):
        print("[controller] scheduler is stopping")
        self.is_running = False

    def pause(self):
        if self.is_paused:
            print("[controller] unpausing")
            self.is_paused = False
        else:
            self.is_paused = True
            time.sleep(self.cycle)
            print("[controller] pausing")

    def help(self):
        print("\nAvailable user commands:")
        for cmd in self.commands:
            print(f" - {cmd}")
        print("")

    def read_config(self):
        print("[controller] paused")
        self.is_paused = True
        time.sleep(1)
        try:
            print("[controller] reading config...")
        except:
            raise Warning("[controller] Unable to read config file")
        print("[controller] unpaused")
        self.is_paused = False
        

m = master()
m.start()
