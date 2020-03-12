import configparser  # https://docs.python.org/3/library/configparser.html
import requests  # https://developers.virustotal.com/v2.0/reference#file-scan
import sqlite3
from datetime import date


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


def hackingabuseipdb(addr):
    conn = sqlite3.connect('attacks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS addresses (address text, numattacks text, lastattack text)''')
    conn.commit()  # saves the queries
    today = date.today()
    day = int(today.strftime("%d"))

    if c.execute("select address from addresses WHERE address=?", (addr,)).fetchone():
        numattacks = c.execute("select numattacks from addresses WHERE address=?", (addr,))
        plusone = int(numattacks.fetchone()[0][0]) + 1
        c.execute("UPDATE addresses SET numattacks = ? WHERE address = ?", (plusone, addr))
        conn.commit()
        #print(c.execute("select * from addresses").fetchall())

        if int(c.execute("select lastattack from addresses where address=?", (addr,)).fetchone()[0]) != day:
            report(addr)
            c.execute("UPDATE addresses SET lastattack = ? WHERE address = ?", (day, addr))
            conn.commit()

    else:
        report(addr)
        c.execute("INSERT INTO addresses (address, numattacks, lastattack) VALUES (?,?,?)", (addr, "1", day))
        conn.commit()
        #print(c.execute("select * from addresses").fetchall())
    conn.commit()  # saves the queries

    conn.close()
