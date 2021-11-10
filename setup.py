"""This is the main file for icarus"""

import os
import curses
import sys
import configparser  # https://docs.python.org/3/library/configparser.html
from multiprocessing import Process
import aiosmtpd.smtp

# Below are my functions.
from app.smtp import startsmtp
from app.editor import editor
from app.udp import runudp
from app.tcp import runtcp
from app.ftp import ftpserver
from app.abuseipdb import largfeed
import app.cfg


# pylint: disable=R0801
config = configparser.ConfigParser()
config.read('icarus.config')
smtpport = config['ADDRESSES']['SMTPPort']
abuseip = config['IPDBAPI']['AbuseIPDB']
abuseapikey = config['IPDBAPI']['IPDBAPI']
vtapikey = config['APIKEY']['apikey']
virustotal = config['APIKEY']['Virustotal']
syslogenable = config['SYSLOG']['Syslog']
syslogip = config['SYSLOG']['IP']
syslogport = config['SYSLOG']['PORT']
largfeedon = config['LARGFEED']['Largfeed']
largfeedserver = config['LARGFEED']['Server']
largfeedport = config['LARGFEED']['Port']
tcpports = config['PORTS']['tcpports']
udpports = config['PORTS']['udpports']

aiosmtpd.smtp.__ident__ = "Microsoft ESMTP MAIL Service"


# pylint: disable=R0915, W0613
def main(window):
    """MAIN!"""
    # Starting SMTP Service
    process2 = Process(name='smtp', target=startsmtp, daemon=True)
    process2.start()
    # startsmtp()
    # Starting FTP Service
    process1 = Process(name='Ftp', target=ftpserver, daemon=True)
    process1.start()
    # Largfeed Queue processor
    if largfeedon != "no":
        process3 = Process(name='largfeed', target=largfeed, daemon=True)
        process3.start()

    # Dynamic low interaction port services.

    for tcpport in tcpports.replace(" ", "").split(','):
        dyntcpprocess = Process(name='DynamicTCP ' + str(tcpport), target=runtcp, daemon=True, args=(int(tcpport),))
        dyntcpprocess.start()

    for udpport in udpports.replace(" ", "").split(','):
        dynudpprocess = Process(name='DynamicUDP ' + str(udpport), target=runudp, daemon=True, args=(int(udpport),))
        dynudpprocess.start()

    while True:
        scurses = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        curses.napms(500)
        # Pretty standard configs. I have the curses refresh set to 3 seconds.
        # https://docs.python.org/3.5/library/curses.html#module-curses
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        sheight, swidth = scurses.getmaxyx()
        cursewinder = curses.newwin(sheight, swidth, 0, 0)
        cursewinder.nodelay(True)
        # No delay fixes a problem of the screen not updating properly.

        # the above 5 are just standard curses commands.
        # First number is vertical, 51 is horizontal
        cursewinder.addstr(0, 51, "Icarus.config")
        cursewinder.addstr(1, 51, "Virustotal:")
        cursewinder.addstr(2, 51, "Enabled: " + virustotal)
        cursewinder.addstr(3, 51, "APIKEY: " + vtapikey)
        cursewinder.addstr(5, 51, "AbuseIPDB:")
        cursewinder.addstr(6, 51, "Enabled: " + abuseip)
        cursewinder.addstr(7, 51, "APIKEY: " + abuseapikey)
        cursewinder.addstr(9, 51, "Syslog:")
        cursewinder.addstr(10, 51, "Enabled: " + syslogenable)
        cursewinder.addstr(11, 51, "Syslog Server: " + syslogip + ":" + syslogport)
        cursewinder.addstr(13, 51, "LARGfeed:")
        cursewinder.addstr(14, 51, "Enabled: " + largfeedon)
        cursewinder.addstr(15, 51, "LARGfeed Server: " + largfeedserver + ":" + largfeedport)
        cursewinder.addstr(17, 51, "Press P to change values.", curses.color_pair(2))
        cursewinder.addstr(18, 51, "Press R to restart.", curses.color_pair(3))
        cursewinder.addstr(19, 51, "Press Q to quit.", curses.color_pair(1))

        cursewinder.addstr(0, 0, "ICARUS HONEYPOT", curses.color_pair(1))

        cursewinder.addstr(12, 0, "Attacks: " + str(app.cfg.numattacks['num']))
        cursewinder.addstr(13, 0, "Last 5 Attackers: ", curses.color_pair(3))
        if app.cfg.attackers:
            for num, address in enumerate(app.cfg.attackers, start=1):
                cursewinder.addstr((num + 13), 0, str(address))

        cursewinder.refresh()

        key = cursewinder.getch()
        if key == ord('q'):
            break
        if key == ord('r'):
            process1.terminate()
            process2.terminate()
            os.execv(sys.executable, ['python3'] + sys.argv)
            # Nice little thing that restarts a python script.
        elif key == ord('p'):
            editor()  # from editor.py, opens your system editor.
            cursewinder.erase()
            cursewinder.refresh()


if __name__ == '__main__':
    curses.wrapper(main)
