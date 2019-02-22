import configparser #https://docs.python.org/3/library/configparser.html
import requests #https://developers.virustotal.com/v2.0/reference#file-scan
import json

def abuseipdb(sessionpeer, mailfrom, mailto):
    config = configparser.ConfigParser()
    config.read('icarus.config')
    abuseip = config['IPDBAPI']['AbuseIPDB']
    apikey = config['IPDBAPI']['IPDBAPI']
    #using configparser to pull the apikey details for abuseipdb.
    headers = { 'Key': apikey,   'Accept': 'application/json', }
    data = {'categories': '11','ip': sessionpeer, 'comment': 'icarus github smtp honeypot'}
    #this is the API. https://docs.abuseipdb.com/#report-endpoint

    if abuseip != "no": #checking if abuseipdb is enabled. Disabled by default. 
        url = "https://api.abuseipdb.com/api/v2/report"

    
        if apikey == "PUT API KEY HERE":
            print ("This is your currently configured APIKEY in smtp.config:\n" + config['IPDBAPI']['IPDBAPI'])
            #I want to convert this to Curses 
        else:
            abusepost = requests.post('https://api.abuseipdb.com/api/v2/report', headers=headers, data=data)
            
          #  print (abusepost)
            if abusepost.status_code != 200:
                print ("HTTP code isn't 200")


