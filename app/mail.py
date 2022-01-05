"""
Send an email to the abuse contact for the IP address behind the scan
"""

import configparser  # https://docs.python.org/3/library/configparser.html
import socket
import time
import ipaddress
from datetime import datetime
import requests  # https://developers.virustotal.com/v2.0/reference#file-scan
import app.cfg

config = configparser.ConfigParser()
config.read('icarus.config')
enabled = config['MAIL']['Mail']