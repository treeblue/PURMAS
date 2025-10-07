import sys
from comms import intranode

#pconfig [OPTION]
#options:
#   stop

def main():
    comm = intranode()
    comm.start()
    comm.connect()
    comm.write("pconfig")
    comm.read()
    if len(sys.argv) > 1:
        comm.write(sys.argv[1])
    else:
        comm.write("none")

if __name__ == "__main__":
    main()