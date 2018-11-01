import socket

from table import *

# client program



# what the client sends to the server
hostnames = read_hns_table("PROJ2-HNS.txt")

# Define the port on which you want to connect to the server
PORT = 65000
# get local hostname
HOST = socket.gethostbyname('localhost')


# connect to RS server

def main():
    buffer = str()
    for h in hostnames:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as rs:
            rs.connect((HOST, PORT))
            rs.sendall(str.encode(h, 'utf-8'))
            resp = DNSEntry.from_str(bytes.decode(rs.recv(1024), 'utf-8'))
            if resp.qtype == '-':
                buffer = buffer + str(h) + " " + "ERROR: HOST NOT FOUND\n"
            else:
                buffer = buffer + str(h) + " " + str(resp.ip) + " " + str(resp.qtype) + "\n"


    with open("RESOLVED.txt", 'w') as file:
        file.write(buffer)


if __name__ == "__main__":
    main()






