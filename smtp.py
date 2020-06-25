import configparser
import socket
from memoryfile import inmemoryfile
from memoryfile import loggingaddresses
from abuseipdb import abuseipdb
from icarussyslog import syslogout
from aiosmtpd.controller import Controller  # the controller that handles async smtp?


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


IP = get_ip_address()
# Found socket at https://docs.python.org/3/library/socket.html mostly just their code.


config = configparser.ConfigParser()
config.read('icarus.config')
if config['ADDRESSES']['IP'] == "auto":
    IP = get_ip_address()
else:
    IP = config['ADDRESSES']['IP']
smtpport = config['ADDRESSES']['SMTPPort']


class smtphoney:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        loggingaddresses(session.peer[0], envelope.mail_from, address)  # check memoryfile.py for this function
        abuseipdb(session.peer[0], envelope.mail_from, address)  # check abuseipdb.py for this function.
        envelope.rcpt_tos.append(address)
        return '250 OK'
        # straight out of documentation

    async def handle_DATA(self, server, session, envelope):
        # box1 = curses.newwin(40, 40, 8, 0)
        # box1.addstr(1, 1, "Last Email:")
        # box1.addstr(2, 1, "IP Address: " + session.peer[0])
        # box1.addstr(3, 1, "From: " + envelope.mail_from)
        # box1.refresh()
        # above box1 code is to show 'last email details' on the screen.
        inmemoryfile(envelope.content.decode('utf8', errors='replace'))  # A function I made in memoryfile.py
        syslogout("Attack: IP:" + session.peer[0])
        return '250 Message accepted for delivery'


def startsmtp():

    controller = Controller(smtphoney(), hostname=IP, port=smtpport)
    # It calls the class below as my handler, the hostname sets the ip, I set the SMTP port to 25 obviously
    controller.start()






