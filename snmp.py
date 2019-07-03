import socketserver


class snmpd(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print ("{} wrote:".format(self.client_address[0]))
        print (data)
        socket.sendto(data.upper(), self.client_address)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), snmpd) as server:
        server.serve_forever()