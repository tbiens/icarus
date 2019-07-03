import socketserver
import asyncio


ServerAddress = ()

class Snmpd(socketserver.DatagramRequestHandler):
    def handle(self):
        print(self.client_address[0])
        #  future proof
        #  self.wfile.write("Message from Server! Hello Client".encode())


if __name__ == "__main__":
    asyncio.run(main())




class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        print('Received %r from %s' % (message, addr))
        print('Send %r to %s' % (message, addr))
        self.transport.sendto(data, addr)


async def main():
    print("Starting UDP server")

    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    # One protocol instance will be created to serve all
    # client requests.
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(),
        local_addr=('0.0.0.0', 161))

    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
        transport.close()


