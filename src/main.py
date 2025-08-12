import time
import threading

class master:
    def __init__(self):
        self.running = False
        self.paused = False
        self.cycle = 1. #sleep time between loop updates
        self.nodes = {}
        self.jobs = {}

    def mainloop(self):
        if self.running: print("[controller] scheduler is running...")
        while self.running:
            if not self.paused:
                None
            # self.stop_condition()
            time.sleep(self.cycle)

    # def stop_condition(self):
    #     if self.i > 5:
    #         self.running = False
    #         print("controller is being stopped")

    def start(self):
        self.running = True
        ctl = threading.Thread(target=self.mainloop)
        ctl.daemon = True
        ctl.start()
        self.take_inputs()
        ctl.join()

    def take_inputs(self):
        while True:
            self.cmd = input("> ")
            if self.cmd == "quit":
                self.running = False
                break
            elif self.cmd == "pause":
                self.pause()
            elif self.cmd == "config":
                self.read_config()
            else:
                print("Unrecognised command")
            time.sleep(self.cycle)

    def pause(self):
        if self.paused:
            print("[controller] unpaused")
            self.paused = False
        else:
            self.paused = True
            time.sleep(self.cycle)
            print("[controller] paused")

    def read_config(self):
        print("[controller] paused")
        self.paused = True
        time.sleep(1)
        try:
            print("[controller] reading config...")
        except:
            raise Warning("[controller] Unable to read config file")
        print("[controller] unpaused")
        self.paused = False
        

m = master()
m.start()
