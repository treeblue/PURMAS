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
    comm.write(sys.argv[1])

if __name__ == "__main__":
    main()