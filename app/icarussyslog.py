"""syslog function that I stopped using."""

import logging
import logging.handlers
from app.config import config


def syslogout(message):
    """ syslog function, not in use."""
    if config.syslogenable != 'no':
        syslog = logging.handlers.SysLogHandler(address=(config.syslogip,int(config.syslogport)))
        log = logging.getLogger(__name__)
        log.setLevel(logging.INFO)
        formatter = logging.Formatter('Icarus Honeypot: %(message)s')
        syslog.setFormatter(formatter)
        log.addHandler(syslog)
        log.info(message)
