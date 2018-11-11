import socket
import sys
from table import *

# client program





# connect to RS server

def main():
    # what the client sends to the server
    hostnames = read_hns_table(sys.argv[2])

    # Define the port on which you want to connect to the server
    PORT = 65000
    # get local hostname
    HOST = socket.gethostbyname(sys.argv[1])

    buffer = str()
    for h in hostnames:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as rs:
                rs.connect((HOST, PORT))
                rs.sendall(str.encode(h, 'utf-8'))
                resp = DNSEntry.from_str(bytes.decode(rs.recv(1024), 'utf-8'))
                if resp.qtype == '-':
                    buffer = buffer + str(h) + " " + "ERROR: HOST NOT FOUND\n"
                else:
                    buffer = buffer + str(h) + " " + str(resp.ip) + " " + str(resp.qtype) + "\n"
        except ConnectionRefusedError:
            print("run rs.py first")
            break


    with open("RESOLVED.txt", 'w') as file:
        file.write(buffer)


if __name__ == "__main__":
    main()






