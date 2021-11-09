import configparser

from app.memoryfile import inmemoryfile
from app.abuseipdb import abuseipdb
from app.icarussyslog import syslogout
from aiosmtpd.controller import Controller  # the controller that handles async smtp?


config = configparser.ConfigParser()
config.read('icarus.config')
if config['ADDRESSES']['IP'] == "auto":
    IP = "0.0.0.0"
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
    controller = Controller(smtphoney(), hostname=IP, port=int(smtpport))
    # It calls the class below as my handler, the hostname sets the ip, I set the SMTP port to 25 obviously
    controller.start()
