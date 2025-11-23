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
org_name = config['MAIL']['Org_name']
zone = config['MAIL']['Timezone']
from_email = config['MAIL']['From_email']
email_port = config['MAIL']['Mail_port']
email_server = config['MAIL']['Mail_server']
email_password = config['MAIL']['Server_password']

def sendEmail(ipaddr, preport):
    server = smtplib.SMTP(email_server, email_port)
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
    logs = "NOTICE: Detected a port scan from " + ipaddr + " to port " + port + " at " + timestamp
    email_body = "Hello,\n\nWe have detected an portscan from an IP address on your computer network. Please review the following logs (which are in " + zone + "):\n\n" + logs + "\n\n\nThank you,\n\n" + org_name
    subject = "Abuse Report: Unauthorized Port Scan"    

    fromaddr = from_email
    toaddr = abuse
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    msg.attach(MIMEText(email_body, 'plain'))

    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(from_email, email_password)

    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)

    print("Done, sent to " + abuse)