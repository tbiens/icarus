import socket
from abuseipdb import hackingabuseipdb


def runsmb():
    while 1:
        s = socket.socket()
        host = '0.0.0.0'
        port = 445
        s.bind((host, port))
        s.listen()

        conn, addr = s.accept()
        # print(conn)
        hackingabuseipdb(addr[0])

        while 1:
            data = conn.recv(1024)
            if not data: break
            #print(data)

        conn.close()
