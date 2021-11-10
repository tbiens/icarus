"""smtp module to accept attachments. only reports the first attachment to virustotal"""

import configparser
from aiosmtpd.controller import Controller  # the controller that handles async smtp?
from app.memoryfile import inmemoryfile
from app.abuseipdb import abuseipdb
from app.icarussyslog import syslogout

# pylint: disable=R0801
config = configparser.ConfigParser()
config.read('icarus.config')
if config['ADDRESSES']['IP'] == "auto":
    IP = "0.0.0.0"
else:
    IP = config['ADDRESSES']['IP']
smtpport = config['ADDRESSES']['SMTPPort']


class SMTPHoney:
    """SMTP async class"""
    # pylint: disable=R0201, R0913, C0103
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        """async documentation"""
        del server  # unused placeholder var
        del rcpt_options  # unused placeholder var
        # check abuseipdb.py for this function.
        abuseipdb(session.peer[0], envelope.mail_from, address)
        envelope.rcpt_tos.append(address)
        return '250 OK'
        # straight out of documentation

    # pylint: disable=R0201, C0103
    async def handle_DATA(self, server, session, envelope):
        """async documentation"""
        del server  # unused placeholder var
        inmemoryfile(envelope.content.decode('utf8', errors='replace'))
        # A function I made in memoryfile.py
        syslogout("Attack: IP:" + session.peer[0])
        return '250 Message accepted for delivery'


def startsmtp():
    """ async controller"""
    controller = Controller(SMTPHoney(), hostname=IP, port=int(smtpport))
    # It calls the class below as my handler.
    controller.start()
