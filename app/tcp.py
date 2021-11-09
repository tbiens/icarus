import socketserver  # https://docs.python.org/3.5/library/socketserver.html
from app.abuseipdb import prereport
from app.memoryfile import lastattacker


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        # self.data = self.request.recv(1024).strip()
        getport = str(self.server.socket).split(",")[5].strip(")>")
        prereport(self.client_address[0], getport)
        lastattacker(self.client_address[0])  # From memoryfile.py


def runtcp(port):

    host = "0.0.0.0"
    server = socketserver.TCPServer((host, port), MyTCPHandler)
    server.allow_reuse_address = True
    server.serve_forever()
