"""dynamic udp service"""

import socketserver
from app.abuseipdb import prereport
from app.memoryfile import lastattacker


class MyUDPHandler(socketserver.BaseRequestHandler):
    """
   socketserver documentation
    """

    def handle(self):

        attackerip = self.client_address[0]
        getport = self.server.server_address[1]
        print(str(attackerip) + str(getport))
        prereport(attackerip, getport)
        lastattacker(attackerip)


def runudp(port):

    with socketserver.UDPServer(('0.0.0.0', port), MyUDPHandler) as server:
        server.allow_reuse_address = True
        server.serve_forever()
