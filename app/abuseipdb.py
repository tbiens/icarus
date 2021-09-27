import configparser  # https://docs.python.org/3/library/configparser.html
import requests  # https://developers.virustotal.com/v2.0/reference#file-scan
import socket
import time
from datetime import datetime
import app.cfg

config = configparser.ConfigParser()
config.read('icarus.config')
abuseip = config['IPDBAPI']['AbuseIPDB']
apikey = config['IPDBAPI']['IPDBAPI']
largfeedserver = config['LARGFEED']['Server']
largfeedport = config['LARGFEED']['Port']


def abuseipdb(sessionpeer, mailfrom, mailto):
    # using configparser to pull the apikey details for abuseipdb.
    headers = {'Key': apikey, 'Accept': 'application/json', }
    data = {'categories': '11, 15', 'ip': sessionpeer,
            'comment': '%s triggered Icarus Smtp honeypot. Check us out on github' % sessionpeer}
    # this is the API. https://docs.abuseipdb.com/#report-endpoint

    if abuseip != "no":  # checking if abuseipdb is enabled. Disabled by default.
        url = "https://api.abuseipdb.com/api/v2/report"

        if apikey != "PUT API KEY HERE":
            abusepost = requests.post(url, headers=headers, data=data)


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
            abusepost = requests.post(url, headers=headers, data=data)


def prereport(addr, port):
    day_of_year = datetime.now().timetuple().tm_yday
    # If we already have the address but no attack today. Report.
    if addr in app.cfg.attackdb:
        if app.cfg.attackdb[addr] != day_of_year:
            report(addr, port)
            app.cfg.largfeedqueue.append(addr)
    # If we don't have the address at all. Report.
    else:
        report(addr, port)
        app.cfg.largfeedqueue.append(addr)
    app.cfg.attackdb[addr] = day_of_year


def largfeed():
    # very straight forward open socket and send bytes data.

    while True:
        try:
            HOST = largfeedserver
            PORT = int(largfeedport)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                if len(app.cfg.largfeedqueue) >= 1:
                    sock.connect((HOST, PORT))
                    addr = app.cfg.largfeedqueue.pop()
                    sock.sendall(bytes(addr + "\n", "utf-8"))
            time.sleep(5)
        except socket.timeout:
            time.sleep(60)

        except socket.error:
            time.sleep(60)
