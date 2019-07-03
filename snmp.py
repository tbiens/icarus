import asyncio
from abuseipdb import snmpabuseipdb
from threading import Thread


class icarus:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        #print(data)
        print(addr[0])
        #snmpabuseipdb(addr[0])
        #message = data.decode()
        #print('Received %r from %s' % (message, addr))
#        print('Send %r to %s' % (message, addr))
#        self.transport.sendto(data, addr)


loop = asyncio.get_event_loop()

listen = loop.create_datagram_endpoint(icarus, local_addr=('0.0.0.0', 161))
transport, protocol = loop.run_until_complete(listen)

t1 = Thread(loop.run_forever())
t1.start()



print ("does this run")
#try:
#
#except KeyboardInterrupt:
#    pass

transport.close()
loop.close()
