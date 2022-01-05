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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ipwhois import IPWhois
import sys
import datetime

config = configparser.ConfigParser()
config.read('icarus.config')
enabled = config['MAIL']['Mail']

def sendEmail(ipaddr, preport):
    obj = IPWhois(ipaddr)
    emails = obj.lookup_whois()["nets"][0]["emails"]

    try:
        abuse = emails[0]
    except:
        print("No abuse contact")
        sys.exit()
    timestamp = datetime.datetime.now()
    prenatport = preport.strip()
    natports = {
        "2021": "21",
        "2022": "22",
        "2023": "23",
        "2205": "25",
        "20110": "110",
        "20111": "111",
        "20135": "135",
        "20139": "139",
        "20143": "143",
        "20161": "161",
        "20445": "445",
        "1433": "1433",
        "1723": "1723",
        "3306": "3306",
        "3389": "3389",
        "5600": "5600",
        "5900": "5900"
    }
    port = natports[prenatport]
    