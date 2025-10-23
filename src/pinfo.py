import sys
import time
from comms import intranode

#pinfo [OPTION]
#options:
#   all
#   nodes
#   jobs

def main():
    comm = intranode()
    comm.start()
    comm.connect()
    comm.write("pinfo")
    comm.read()

    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        mode = "all"
    comm.write(mode)
    
    if mode == "all" or mode == "nodes":
        print("Node\t| IP\t\t| Status")
        msg = ""
        new_msg = comm.read()
        while new_msg != "done":
            comm.write("next")
            if msg != new_msg:
                msg = new_msg
                print(msg)
            new_msg = comm.read()
        comm.write("next")

    if mode == "all":
        print("")

    if mode == "all" or mode == "jobs":
        print("Job ID\t| File")
        msg = ""
        new_msg = comm.read()
        while new_msg != "done":
            comm.write("next")
            if msg != new_msg:
                msg = new_msg
                print(msg)
            new_msg = comm.read()
        comm.write("next")
        
        

if __name__ == "__main__":
    main()