import socket #To get your IP address for the server to run on.
import curses
import sys
import configparser #https://docs.python.org/3/library/configparser.html
from time import sleep
from aiosmtpd.controller import Controller #the controller that handles async smtp?
import aiosmtpd.smtp
from memoryfile import inmemoryfile
from memoryfile import loggingaddresses
from abuseipdb import abuseipdb
from icarussyslog import syslogout
from editor import editor
from snmp import runsnmp
from smb import runsmb
from multiprocessing import Process, Lock


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


IP = get_ip_address()

# Found socket at https://docs.python.org/3/library/socket.html mostly just their code.

config = configparser.ConfigParser()
config.read('icarus.config')
abuseip = config['IPDBAPI']['AbuseIPDB']
abuseapikey = config['IPDBAPI']['IPDBAPI']
vtapikey = config['APIKEY']['apikey']
virustotal = config['APIKEY']['Virustotal']
syslogenable = config['SYSLOG']['Syslog']
syslogip = config['SYSLOG']['IP']
syslogport = config['SYSLOG']['PORT']

aiosmtpd.smtp.__ident__ = "Microsoft ESMTP MAIL Service"


def main(window):
    controller = Controller(smtphoney(), hostname=IP, port=25)
    # It calls the class below as my handler, the hostname sets the ip, I set the SMTP port to 25 obviously
    controller.start()
    lock = Lock()
    p1 = Process(name='Snmp', target=runsnmp, daemon=True)
    p1.start()
    p2 = Process(name='Smb', target=runsmb, daemon=True)
    p2.start()

    while True:

        s = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        # the above 3 items for curse are just standard config.
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK);
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK);
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK);
        # I want the 'press Q to quit' to be red
        sh, sw = s.getmaxyx()
        w = curses.newwin(sh, sw, 0, 0)
        w.keypad(1)

        # the above 5 are just standard curses commands.
        # First number is vertical, 51 is horizontal
        w.addstr(0, 51, "Icarus.config")
        w.addstr(1, 51, "Virustotal:")
        w.addstr(2, 51, "Enabled: " + virustotal)
        w.addstr(3, 51, "APIKEY: " + vtapikey)
        w.addstr(5, 51, "AbuseIPDB:")
        w.addstr(6, 51, "Enabled: " + abuseip)
        w.addstr(7, 51, "APIKEY: " + abuseapikey)
        w.addstr(9, 51, "Syslog:")
        w.addstr(10, 51, "Enabled: " + syslogenable)
        w.addstr(11, 51, "Syslog Server: " + syslogip + ":" + syslogport)
        w.addstr(13, 51, "Press P to change values.", curses.color_pair(2))
        w.addstr(14, 51, "Press R to reset screen.", curses.color_pair(3))
        w.addstr(15, 51, "Press A to restart services.", curses.color_pair(1))

        w.addstr(0, 0, "Listening on: " + IP)
        w.addstr(1, 0, "Server started. Press Q to quit.", curses.color_pair(1))
        w.addstr(2, 0, "SNMP Running: " + str(p1.is_alive()))
        w.addstr(3, 0, "SMB Running:  " + str(p2.is_alive()))
        # It always shows IP address it's listening on and showing you can hit Q to quit.

        w.refresh()

        key = w.getch()
        if key == ord('q'):
            break
        elif key == ord('r'):
            w.erase()
            w.refresh()
        elif key == ord('a'):
            import os
            os.execv(sys.executable, ['python' + sys.argv])
        elif key == ord('p'):
            editor()  # from editor.py, opens your system editor.
            w.erase()
            w.refresh()
            # window.addstr(2,0,"You pressed P\n") # Just a place holder for new commands in the future.

        sleep(1)  # So that the screen isn't refreshing at crazy rates unnecessarily.

    # threading just wouldnt work. Process does seem to work.
    controller.stop()
    p1.terminate()
    p2.terminate()


class smtphoney:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        loggingaddresses(session.peer[0], envelope.mail_from, address)  # check memoryfile.py for this function
        abuseipdb(session.peer[0], envelope.mail_from, address)  # check abuseipdb.py for this function.
        envelope.rcpt_tos.append(address)
        return '250 OK'
        # straight out of documentation

    async def handle_DATA(self, server, session, envelope):
        box1 = curses.newwin(40,40,5,0)
        box1.addstr(1,1,"Last Email:")
        box1.addstr(2,1,"IP Address: " + session.peer[0])
        box1.addstr(3,1,"From: " + envelope.mail_from)
        box1.refresh()
        # above box1 code is to show 'last email details' on the screen.
        inmemoryfile(envelope.content.decode('utf8', errors='replace'))  # A function I made in memoryfile.py
        syslogout("Attack: IP:" + session.peer[0])
        return '250 Message accepted for delivery'


if __name__ == '__main__':
    curses.wrapper(main)




