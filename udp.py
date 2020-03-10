import asyncio
from abuseipdb import hackingabuseipdb
from memoryfile import lastattacker


class icarus:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        hackingabuseipdb(addr[0])
        lastattacker(addr[0])


def runudp():
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    listen = loop.create_datagram_endpoint(icarus, local_addr=('0.0.0.0', 161))
    transport, protocol = loop.run_until_complete(listen)

    loop.run_forever()
    transport.close()
    loop.close()



