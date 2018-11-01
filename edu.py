import socket

from table import Table

# data
HOST = ''
PORT = 65001

###


# load shit from DNS table DNSRS.txt
ts_table = Table('PROJ2-DNSCOM.txt')

print("[S]: Server DNS table:", ts_table)

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
                        match = [entry for entry in ts_table if entry.hostname == data]
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
                                file.write(data)

                            print("[S]: Sending error message to client...")

                            msg = str("- - 0 -").encode('utf-8')
                            conn.send(msg)
