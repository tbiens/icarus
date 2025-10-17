import configparser

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('icarus.config')


        self.abuseip = self.config['IPDBAPI']['AbuseIPDB']
        self.abuseapikey = self.config['IPDBAPI']['IPDBAPI']
        self.vtapikey = self.config['APIKEY']['apikey']
        self.virustotal = self.config['APIKEY']['Virustotal']
        self.syslogenable = self.config['SYSLOG']['Syslog']
        self.syslogip = self.config['SYSLOG']['IP']
        self.syslogport = self.config['SYSLOG']['PORT']
        self.largfeedon = self.config['LARGFEED']['Largfeed']
        self.largfeedserver = self.config['LARGFEED']['Server']
        self.largfeedport = self.config['LARGFEED']['Port']
        self.httpposton = self.config['HTTPPOST']['Httppost']
        self.httpposturl = self.config['HTTPPOST']['url']
        self.tcpports = self.config['PORTS']['tcpports']
        self.udpports = self.config['PORTS']['udpports']

config = Config()
