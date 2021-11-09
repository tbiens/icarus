import configparser

import app.cfg
from app.memoryfile import inmemoryfile
from app.abuseipdb import abuseipdb
from app.icarussyslog import syslogout
from aiosmtpd.controller import Controller  # the controller that handles async smtp?


IP = app.cfg.ipaddress[0]
# Found socket at https://docs.python.org/3/library/socket.html mostly just their code.


config = configparser.ConfigParser()
config.read('icarus.config')
if config['ADDRESSES']['IP'] == "auto":
    IP = app.cfg.ipaddress[0]
else:
    IP = config['ADDRESSES']['IP']
smtpport = config['ADDRESSES']['SMTPPort']


class smtphoney:
    # pylint: disable=R0201, R0913
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        del server  # unused placeholder var
        del rcpt_options  # unused placeholder var
        abuseipdb(session.peer[0], envelope.mail_from, address)  # check abuseipdb.py for this function.
        envelope.rcpt_tos.append(address)
        return '250 OK'
        # straight out of documentation

    # pylint: disable=R0201
    async def handle_DATA(self, server, session, envelope):
        del server  # unused placeholder var
        inmemoryfile(envelope.content.decode('utf8', errors='replace'))  # A function I made in memoryfile.py
        syslogout("Attack: IP:" + session.peer[0])
        return '250 Message accepted for delivery'


def startsmtp():
    controller = Controller(smtphoney(), hostname=IP, port=smtpport)
    # It calls the class below as my handler, the hostname sets the ip, I set the SMTP port to 25 obviously
    controller.start()
