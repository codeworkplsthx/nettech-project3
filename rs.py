import socket

from table import Table

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
                            print("[S]: No match for " + data + "in DNS table...")
                            with open("log.txt", 'w+') as file:
                                file.writelines(data)
                            ns_server = [dns_entry for dns_entry in rs_table if dns_entry.qtype == 'NS'][0]
                            print("[S]: Sending error message to client...")

                            msg = str(ns_server).encode('utf-8')
                            conn.send(msg)
