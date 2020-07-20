import asyncio
from app.abuseipdb import prereport
from app.memoryfile import lastattacker


class icarus:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        prereport(addr[0])
        lastattacker(addr[0])


def runudp(port):
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    listen = loop.create_datagram_endpoint(icarus, local_addr=('0.0.0.0', port))
    transport, protocol = loop.run_until_complete(listen)

    loop.run_forever()
    transport.close()
    loop.close()



