# import sys
import time
from comms import intranode

def main():
    comm = intranode()
    comm.start()
    comm.connect()
    comm.write("pinfo")
    
    print("Node\t| IP\t\t| Status")
    msg = comm.read()
    new_msg = comm.read()
    while new_msg != "done":
        
        if msg != new_msg:
            msg = new_msg
            print(msg)
        new_msg = comm.read()
        time.sleep(0.1)
        
        
        

if __name__ == "__main__":
    main()