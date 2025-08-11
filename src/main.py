import time
import threading

class master:
    def __init__(self):
        self.running = False
        self.pause = False
        self.i = 0

    def mainloop(self):
        if self.running: print("[controller] scheduler is running...")
        while self.running:
            if not self.pause:
                None
            self.stop_condition()
            time.sleep(1)

    def stop_condition(self):
        if self.i > 5:
            self.running = False
            print("controller is being stopped")

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
            time.sleep(1)

m = master()
m.start()
