from comms import intranode

def main():
    comm = intranode()
    comm.start()
    comm.connect()
    comm.write("Hello World?")
    # comm.close()

if __name__ == "__main__":
    main()