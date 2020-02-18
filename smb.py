import socketserver
import time
from abuseipdb import hackingabuseipdb



class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        hackingabuseipdb(self.client_address[0])


def runsmb():
    HOST, PORT = "0.0.0.0", 445

    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    server.serve_forever()