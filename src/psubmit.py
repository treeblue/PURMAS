import sys
import time
from comms import intranode

def main():
    if len(sys.argv) == 1:
        raise Exception("Please specify a job script")
    else:
        for arg in sys.argv[1:]:
            if ".sh" not in arg:
                raise Exception("must submit a .sh script")
    comm = intranode()
    comm.start()
    comm.connect()
    comm.write("psubmit")

    comm.read()
    for arg in sys.argv[1:]:
        comm.write(arg)
        time.sleep(0.01) #this wont work for slow systems!!!!
    comm.write("done")

if __name__ == "__main__":
    main()