import socket

from table import Table
from dnsentry import *

HOST = ''
PORT = 65000



rs_table = Table('PROJ2-DNSRS.txt')

print("[S]: Server host name is: ", socket.gethostname())
print("[S]: Server IP address is  ", socket.gethostbyname('localhost'))
print("[S]: Server DNS table:", rs_table)

# create portal for clients
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(PORT)

    while True:
        conn, addr = s.accept()
        if not conn:
            break
        else:
            with conn:
                print("[S]: Got a connection request from + " + str(conn) + " at " + str(addr))
                while True:
                    data = conn.recv(1024)

                    if not data:
                        break
                    else:
                        data = bytes.decode(data, 'utf-8')
                        print('Received ' + data)

                        print("[S]: Looking up hostname " + data + " in DNS table...")
                        # case: hostname is in table
                        match = [entry for entry in rs_table if entry.hostname == data]
                        if match:
                            # send matching dns entry to client
                            print("[S]: Found " + str(match))
                            msg = str.encode(str(match), 'utf-8')
                            print("[S]: Sending " + str(msg) + " to client...")
                            conn.send(msg)
                        # case: hostname is not in table
                        else:
                            ext = data[-4:]


                            #case: hostname is .com
                            if ext == ".com":
                                print("[S]: Hostname has ext " + ext)
                                for dns_entry in rs_table:
                                    if dns_entry.qtype == 'NS' and int(dns_entry.port) == 65001:
                                        com_server = dns_entry

                                print("[S]: Connecting to  " + repr(com_server))
                                print(com_server)
                                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as com:
                                    com.connect(('',com_server.port))
                                    com.sendall(str.encode(data, 'utf-8'))
                                    resp = com.recv(1024)
                                    conn.sendall(resp)
                            elif ext == ".edu":
                                print("[S]: Hostname has ext " + ext)
                                for dns_entry in rs_table:
                                    if dns_entry.qtype == 'NS' and int(dns_entry.port) == 65002:
                                        edu_server = dns_entry

                                print(edu_server)
                                print("[S]: Connecting to  " + repr(edu_server))
                                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as edu:
                                    edu.connect(('',int(edu_server.port)))
                                    edu.sendall(str.encode(data, 'utf-8'))
                                    resp = edu.recv(1024)
                                    conn.sendall(resp)
                            # case: hostname is not .com or .edu
                            elif ext != ".com" and ext != ".edu":

                                print("[S]: No match for " + data + " in DNS table...")
                                with open("log.txt", 'w+') as file:
                                    file.writelines(data)
                                print("[S]: Sending error message to client...")
                                msg = str("- - 0 -").encode('utf-8')
                                conn.send(msg)





