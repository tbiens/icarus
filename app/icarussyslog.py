"""syslog function that I stopped using."""

import logging
import logging.handlers
import configparser  # https://docs.python.org/3/library/configparser.html


config = configparser.ConfigParser()
config.read('icarus.config')
syslogenable = config['SYSLOG']['Syslog']
syslogip = config['SYSLOG']['IP']
syslogport = config['SYSLOG']['PORT']


def syslogout(message):
    """ syslog function, not in use."""
    if syslogenable != 'no':
        syslog = logging.handlers.SysLogHandler(address=(syslogip,int(syslogport)))
        log = logging.getLogger(__name__)
        log.setLevel(logging.INFO)
        formatter = logging.Formatter('Icarus Honeypot: %(message)s')
        syslog.setFormatter(formatter)
        log.addHandler(syslog)
        log.info(message)
