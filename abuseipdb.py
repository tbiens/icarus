import configparser  # https://docs.python.org/3/library/configparser.html
import requests  # https://developers.virustotal.com/v2.0/reference#file-scan
import socket
import sqlite3
from datetime import datetime


def abuseipdb(sessionpeer, mailfrom, mailto):
    config = configparser.ConfigParser()
    config.read('icarus.config')
    abuseip = config['IPDBAPI']['AbuseIPDB']
    apikey = config['IPDBAPI']['IPDBAPI']
    # using configparser to pull the apikey details for abuseipdb.
    headers = {'Key': apikey, 'Accept': 'application/json', }
    data = {'categories': '11', 'ip': sessionpeer, 'comment': 'Icarus Smtp honeypot github'}
    # this is the API. https://docs.abuseipdb.com/#report-endpoint

    if abuseip != "no":  # checking if abuseipdb is enabled. Disabled by default.
        url = "https://api.abuseipdb.com/api/v2/report"

        if apikey != "PUT API KEY HERE":
            abusepost = requests.post(url, headers=headers, data=data)


def report(ip):
    config = configparser.ConfigParser()
    config.read('icarus.config')
    abuseip = config['IPDBAPI']['AbuseIPDB']
    apikey = config['IPDBAPI']['IPDBAPI']
    # using configparser to pull the apikey details for abuseipdb.
    headers = {'Key': apikey, 'Accept': 'application/json', }
    data = {'categories': '15', 'ip': ip, 'comment': 'Icarus honeypot on github'}
    # this is the API. https://docs.abuseipdb.com/#report-endpoint

    if abuseip != "no":  # checking if abuseipdb is enabled. Disabled by default.
        url = "https://api.abuseipdb.com/api/v2/report"

        if apikey != "PUT API KEY HERE":
            abusepost = requests.post(url, headers=headers, data=data)


def prereport(addr):
    conn = sqlite3.connect('attacks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS addresses (address text, numattacks integer, lastattack integer)''')
    conn.commit()  # saves the queries
    #  If the database doesn't yet exist.

    day_of_year = datetime.now().timetuple().tm_yday

    if c.execute("select address from addresses WHERE address=?", (addr,)).fetchone():
        numattacks = c.execute("select numattacks from addresses WHERE address=?", (addr,))
        beforeone = numattacks.fetchone()[0]
        plusone = beforeone + 1
        # print(plusone)
        c.execute("UPDATE addresses SET numattacks = ? WHERE address = ?", (plusone, addr))
        conn.commit()
        # If the attacker already exists; just update number of attacks.

        if int(c.execute("select lastattack from addresses where address=?", (addr,)).fetchone()[0]) != day_of_year:
            report(addr)
            largfeed(addr)
            c.execute("UPDATE addresses SET lastattack = ? WHERE address = ?", (day_of_year, addr))
            conn.commit()
            # If the last attack wasn't today.

    else:
        report(addr)
        largfeed(addr)
        c.execute("INSERT INTO addresses (address, numattacks, lastattack) VALUES (?,?,?)", (addr, "1", day_of_year))
        conn.commit()
        # If the attacking IP hasn't been seen before.

    conn.commit()  # saves the queries
    conn.close()


def largfeed(addr):
    config = configparser.ConfigParser()
    config.read('icarus.config')
    largfeedon = config['LARGFEED']['Largfeed']
    largfeedserver = config['LARGFEED']['Server']
    largfeedport = config['LARGFEED']['Port']

    if largfeedon != "no":
        HOST = largfeedserver
        PORT = int(largfeedport)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(bytes(addr + "\n", "utf-8"))



