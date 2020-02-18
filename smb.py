import socket
from socket import error as socketerror
import time
from abuseipdb import hackingabuseipdb



def runsmb():
    while 1:

        try:
            while 1:
                s = socket.socket()
                host = '0.0.0.0'
                port = 445
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((host, port))
                s.listen()

                conn, addr = s.accept()
                # print(conn)
                hackingabuseipdb(addr[0])
                lastattacker(addr[0])

                while 1:
                    data = conn.recv(1024)
                    if not data: break
                    #print(data)

                conn.close()
                time.sleep(1)
        except socketerror:
            pass
