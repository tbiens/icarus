import asyncio
from app.abuseipdb import prereport
from app.memoryfile import lastattacker


class icarus:
    # pylint: disable=R0201, W0201
    def connection_made(self, transport):
        self.transport = transport
        # from asyncio documentation

    def datagram_received(self, data, addr):
        del data  # unused var place holder
        prereport(addr[0], addr[1])
        lastattacker(addr[0])


def runudp(port):
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    listen = loop.create_datagram_endpoint(icarus, local_addr=('0.0.0.0', port))
    transport, protocol = loop.run_until_complete(listen)
    del protocol  # unused placeholder var.
    loop.run_forever()
    transport.close()
    loop.close()
