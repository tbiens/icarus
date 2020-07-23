import configparser
import socket
from app.memoryfile import inmemoryfile
from app.abuseipdb import abuseipdb
from app.icarussyslog import syslogout
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
        abuseipdb(session.peer[0], envelope.mail_from, address)  # check abuseipdb.py for this function.
        envelope.rcpt_tos.append(address)
        return '250 OK'
        # straight out of documentation

    async def handle_DATA(self, server, session, envelope):
        inmemoryfile(envelope.content.decode('utf8', errors='replace'))  # A function I made in memoryfile.py
        syslogout("Attack: IP:" + session.peer[0])
        return '250 Message accepted for delivery'


def startsmtp():
    controller = Controller(smtphoney(), hostname=IP, port=smtpport)
    # It calls the class below as my handler, the hostname sets the ip, I set the SMTP port to 25 obviously
    controller.start()

