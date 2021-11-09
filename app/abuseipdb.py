import configparser  # https://docs.python.org/3/library/configparser.html
import requests  # https://developers.virustotal.com/v2.0/reference#file-scan
import socket
import time
import ipaddress
from datetime import datetime
import app.cfg

config = configparser.ConfigParser()
config.read('icarus.config')
abuseip = config['IPDBAPI']['AbuseIPDB']
apikey = config['IPDBAPI']['IPDBAPI']
largfeedserver = config['LARGFEED']['Server']
largfeedport = config['LARGFEED']['Port']


def checkwhitelist(ipaddr):
    # We wont add our own ips or select others.
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
    del mailfrom  # unused var placeholder
    del mailto  # unused var placeholder
    # using configparser to pull the apikey details for abuseipdb.
    headers = {'Key': apikey, 'Accept': 'application/json', }
    data = {'categories': '11, 15', 'ip': sessionpeer,
            'comment': '%s triggered Icarus Smtp honeypot. Check us out on github' % sessionpeer}
    # this is the API. https://docs.abuseipdb.com/#report-endpoint

    if abuseip != "no":  # checking if abuseipdb is enabled. Disabled by default.
        url = "https://api.abuseipdb.com/api/v2/report"

        if apikey != "PUT API KEY HERE":
            requests.post(url, headers=headers, data=data)


def report(ip, preport):
    # Docker NAT reports wrong port.
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

    # using configparser to pull the apikey details for abuseipdb.
    headers = {'Key': apikey, 'Accept': 'application/json', }
    data = {'categories': '14, 15', 'ip': ip,
            'comment': '%s triggered Icarus honeypot on port %s. Check us out on github.' % (ip, port,)}
    # this is the API. https://docs.abuseipdb.com/#report-endpoint

    if abuseip != "no":  # checking if abuseipdb is enabled. Disabled by default.
        url = "https://api.abuseipdb.com/api/v2/report"

        if apikey != "PUT API KEY HERE":
            requests.post(url, headers=headers, data=data)


def prereport(addr, port):
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
    # very straight forward open socket and send bytes data.
    # TODO API Key

    whitelisturl = "http://" + largfeedserver + "/whitelist.txt"
    wlu = requests.get(whitelisturl)
    for whitelistline in wlu.text.split('\n'):
        if whitelistline:
            if str("#") in whitelistline:
                pass
            else:
                app.cfg.whitelist.append(whitelistline)

    while True:
        try:
            host = largfeedserver
            port = int(largfeedport)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                if len(app.cfg.largfeedqueue) >= 1:

                    addr = app.cfg.largfeedqueue.pop()
                    if checkwhitelist(addr):
                        sock.connect((host, port))
                        sock.sendall(bytes(addr + "\n", "utf-8"))
                    else:
                        pass
            time.sleep(5)
        except socket.timeout:
            time.sleep(60)

        except socket.error:
            time.sleep(60)
