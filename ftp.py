import os
import hashlib
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer
from virustotal import virustotalfile
from abuseipdb import hackingabuseipdb


class MyHandler(FTPHandler):

    def on_connect(self):
        hackingabuseipdb(self.remote_ip)

    def on_file_received(self, file):
        # do something when a file has been received
        # print(file)
        with open(file, mode='rb') as filecontents:
            # print(filecontents.read())
            shahash = hashlib.sha256(filecontents.read()).hexdigest()
            # print(shahash)
        os.rename(file, "./downloads/" + shahash)
        virustotalfile("./downloads/" + shahash)

    def on_incomplete_file_sent(self, file):
        # do something when a file is partially sent
        os.remove(file)

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        os.remove(file)


def ftpserver():
    authorizer = DummyAuthorizer()
    # authorizer.add_user('user', '12345', homedir='./downloads', perm='elradfmwMT')
    authorizer.add_anonymous(homedir='./downloads', perm="adfw")

    handler = MyHandler
    handler.authorizer = authorizer
    server = FTPServer(('', 21), handler)
    server.serve_forever()
