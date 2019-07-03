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


def runsnmp():
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    listen = loop.create_datagram_endpoint(icarus, local_addr=('0.0.0.0', 161))
    transport, protocol = loop.run_until_complete(listen)

    loop.run_forever()
    transport.close()
    loop.close()


t1 = Thread(target=runsnmp,name= "t1")
print("what")
t1.start()
print("after t1")
