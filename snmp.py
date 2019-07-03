import socketserver
import threading


ServerAddress = ("0.0.0.0", 161)

class Snmpd(socketserver.DatagramRequestHandler):
    def handle(self):
        print(self.client_address[0])
        #  future proof
        #  self.wfile.write("Message from Server! Hello Client".encode())


#if __name__ == "__main__":


SnmpdServerObject = socketserver.ThreadingUDPServer(ServerAddress, Snmpd)
SnmpdServerObject.serve_forever()
