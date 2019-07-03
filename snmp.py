import socketserver
import threading


ServerAddress = ("0.0.0.0", 161)


class snmpd(socketserver.BaseRequestHandler):
    def handle(self):
        #  data = self.request[0].strip()
        #  socket = self.request[1]
        #  placeholders incase I want them back.
        print(self.client_address[0])
#      print (data)
#        socket.sendto("bob", self.client_address)


class Snmpd(socketserver.DatagramRequestHandler):
    def handle(self):
        print(self.client_address[0])
        #  future proof
        #  self.wfile.write("Message from Server! Hello Client".encode())


#if __name__ == "__main__":


SnmpdServerObject = socketserver.ThreadingUDPServer(ServerAddress, Snmpd)
SnmpdServerObject.serve_forever()
