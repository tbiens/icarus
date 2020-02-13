import asyncio
import logging
from abuseipdb import snmpabuseipdb


class icarus:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        #print(data)
        #print(addr[0])
        snmpabuseipdb(addr[0])
        #message = data.decode()
        #print('Received %r from %s' % (message, addr))
#        print('Send %r to %s' % (message, addr))
#        self.transport.sendto(data, addr)


def runsnmp():
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    listen = loop.create_datagram_endpoint(icarus, local_addr=('0.0.0.0', 161))
    transport, protocol = loop.run_until_complete(listen)

    loop.run_forever()
    transport.close()
    loop.close()


def runsmb(ip='0.0.0.0', port=445):
    loop = asyncio.get_event_loop()
    smb = asyncio.start_server(icarus, ip, port)
    server = loop.run_until_complete(smb)
    logging.info('Looking for connections on {}'.format(
        server.sockets[0].getsockname()))

    try:
        logging.info("Press Control-C to stop the server.")
        loop.run_until_complete(smb)
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt received: closing the server.")
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

runsmb()