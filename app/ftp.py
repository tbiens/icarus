"""ftp protocol is meant to accept files and upload to virustotal"""

import os
import hashlib
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer
from app.virustotal import virustotalfile
from app.abuseipdb import prereport


class MyHandler(FTPHandler):
    """Mainly the pyftpd library"""

    def on_connect(self):
        prereport(self.remote_ip, "21")

    def on_file_received(self, file):
        # do something when a file has been received
        # print(file)
        with open(file, mode='rb') as filecontents:
            # print(filecontents.read())
            shahash = hashlib.sha256(filecontents.read()).hexdigest()
            # print(shahash)
            filecontents.close()
        if os.path.isfile("./downloads/" + shahash):
            os.remove(file)
        else:
            os.rename(file, "./downloads/" + shahash)
            virustotalfile(shahash)

    def on_incomplete_file_sent(self, file):
        # do something when a file is partially sent
        os.remove(file)

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        os.remove(file)


def ftpserver():
    """The function that opens a port."""
    authorizer = DummyAuthorizer()
    # authorizer.add_user('user', '12345', homedir='./downloads', perm='elradfmwMT')
    authorizer.add_anonymous(homedir='./downloads', perm="adfw")

    handler = MyHandler
    handler.authorizer = authorizer
    server = FTPServer(('', 2021), handler)
    server.serve_forever()
