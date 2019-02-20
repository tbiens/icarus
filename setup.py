
import asyncio # https://aiosmtpd.readthedocs.io/en/latest/aiosmtpd/docs/controller.html
import aiosmtpd # the smtp library
import socket #To get your IP address for the server to run on.
import curses
from aiosmtpd.controller import Controller #the controller that handles async smtp?
from memoryfile import inmemoryfile
from memoryfile import loggingaddresses
from abuseipdb import abuseipdb

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

IP = get_ip_address()

#Found socket at https://docs.python.org/3/library/socket.html mostly just their code.



def main(window):
    curses.curs_set(0)
    stdscr = curses.initscr()
    curses.noecho()
    while True:
        window.clear()
        print ("Listening on:" + IP)
        print ("Server started. Press Q to quit.")
        c = stdscr.getch()
        if c == ord('q'):
            break
        elif c == ord('p'):
            print ("You pressed P")
        controller = Controller(smtphoney(), hostname = IP,port=25)
#It calls the class above as my handler, the hostname sets the ip, I set the SMTP port to 25 obviously
        controller.start()
        input("Server started. Press Return to quit.")
        controller.stop()
        window.refresh()
        time.sleep(0.2)




class smtphoney:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        loggingaddresses(session.peer[0], envelope.mail_from, address)
        abuseipdb(session.peer[0], envelope.mail_from, address)
        envelope.rcpt_tos.append(address)
        return '250 OK'
        #straight out of documentation

    async def handle_DATA(self, server, session, envelope):
        print ('New Email \n')
        inmemoryfile(envelope.content.decode('utf8', errors='replace')) #A function I made in memoryfile.py
        print('End of message')
        return '250 Message accepted for delivery'
    
if __name__ == '__main__':
    curses.wrapper(main)




