import socket
import sys
from table import Table


# data
HOST = ''
PORT = 65002

###

import sys

def main():



    # load shit from DNS table DNSCOM.txt
    ts_table = Table(sys.argv[1])
    print("[S]: Server host name is: ", socket.gethostname())
    print("[S]: Server IP address is  ", socket.gethostbyname('localhost'))
    print("[S]: Listening on: ",PORT)
    print("[S]: Server DNS table:", ts_table)

    # create portal for clients (RS server)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(PORT)


        while True:
            conn = None
            try:
                conn, addr = s.accept()
                if not conn:
                    break
                else:
                    with conn: # socket to client
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
            except KeyboardInterrupt:
                if conn:
                    conn.close()
                break


if __name__ == "__main__":
    main()
