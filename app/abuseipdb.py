"""
Contains functions to report to abuseipdb api.
"""

import logging
import configparser  # https://docs.python.org/3/library/configparser.html
import socket
import time
import ipaddress
from datetime import datetime
import requests  # https://developers.virustotal.com/v2.0/reference#file-scan
import app.cfg

from app.config import config

config = config


def checkwhitelist(ipaddr):
    """We wont add our own ips or select others."""
    register = 0
    if ipaddr:
        sipaddr = ipaddr.strip()
        for subnet in app.cfg.whitelist:
            if ipaddress.IPv4Address(sipaddr) not in ipaddress.IPv4Network(subnet):
                register += 1
            else:
                # log2console("IP in whitelist: " + sipaddr)
                pass
        if register == len(app.cfg.whitelist):
            # print(register)
            return 1
    return None


def abuseipdb(sessionpeer, mailfrom, mailto):
    """Function to send to abuseipdb"""
    del mailfrom  # unused var placeholder
    del mailto  # unused var placeholder
    # using configparser to pull the apikey details for abuseipdb.
    headers = {'Key': config.abuseapikey, 'Accept': 'application/json', }
    data = {'categories': '11, 15', 'ip': sessionpeer,
            'comment': f'{sessionpeer} triggered Icarus Smtp honeypot. Check us out on github'}
    # this is the API. https://docs.abuseipdb.com/#report-endpoint

    if config.abuseip != "no":  # checking if abuseipdb is enabled. Disabled by default.
        url = "https://api.abuseipdb.com/api/v2/report"

        if config.abuseapikey != "PUT API KEY HERE":
            requests.post(url, headers=headers, data=data)


def report(ipaddr, preport):
    """Function to send to abuseipdb. Docker NAT reports wrong port."""
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
    if prenatport not in natports:
        return
    port = natports[prenatport]

    # using configparser to pull the apikey details for abuseipdb.
    headers = {'Key': config.abuseapikey, 'Accept': 'application/json', }
    data = {'categories': '14, 15', 'ip': ipaddr,
            'comment': f'{ipaddr} triggered Icarus honeypot on port {port}. Check us out on github.'}
    # this is the API. https://docs.abuseipdb.com/#report-endpoint

    if config.abuseip != "no":  # checking if abuseipdb is enabled. Disabled by default.
        url = "https://api.abuseipdb.com/api/v2/report"

        if config.abuseapikey != "PUT API KEY HERE":
            requests.post(url, headers=headers, data=data)


def prereport(addr, port):
    """Processing reports to ensure we arent reporting ips too often."""
    day_of_year = datetime.now().timetuple().tm_yday
    # If we already have the address but no attack today. Report.
    if addr in app.cfg.attackdb:
        if app.cfg.attackdb[addr] != day_of_year:
            if checkwhitelist(addr):
                report(addr, port)
                app.cfg.largfeedqueue.append(addr)
            else:
                pass

    # If we don't have the address at all. Report.
    else:
        report(addr, port)
        app.cfg.largfeedqueue.append(addr)
    app.cfg.attackdb[addr] = day_of_year


def largfeed():
    """very straight forward open socket and send bytes data. Largfeed takes it from there."""
    # TODO API Key and crypto
    try:
        whitelisturl = "https://" + config.largfeedserver + "/whitelist.txt"
        wlu = requests.get(whitelisturl, verify=False)
        wlu.raise_for_status()
        for whitelistline in wlu.text.split('\n'):
            if whitelistline and not whitelistline.startswith("#"):
                app.cfg.whitelist.append(whitelistline)
    except requests.exceptions.RequestException as e:
        logging.error(f"Could not download whitelist for largfeed: {e}")

    while True:
        try:
            host = config.largfeedserver
            port = int(config.largfeedport)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                if len(app.cfg.largfeedqueue) >= 1:

                    addr = app.cfg.largfeedqueue.pop()
                    if checkwhitelist(addr):
                        sock.connect((host, port))
                        sock.sendall(bytes(addr + "\n", "utf-8"))
                    else:
                        pass
            time.sleep(5)
        except socket.gaierror as e:
            logging.error(f"DNS error in largfeed: {e}")
            time.sleep(60)
        except ConnectionRefusedError:
            logging.error("Connection refused in largfeed")
            time.sleep(60)
        except socket.timeout:
            logging.warning("Socket timeout in largfeed")
            time.sleep(60)
        except socket.error as e:
            logging.error(f"Socket error in largfeed: {e}")
            time.sleep(60)

def httppost():
    while True:
        try:
            url = config.httpposturl

            if len(app.cfg.largfeedqueue) >= 1:

                addr = app.cfg.largfeedqueue.pop()

                data = {"ip_address": addr, "reason": "Icarus reliable report"}
                response = requests.post(url, data=data)
                response.raise_for_status()
                # print(response.text)

            time.sleep(5)

        except requests.exceptions.RequestException as e:
            logging.error(f"Could not post to {url}: {e}")
            time.sleep(60)
