import configparser #https://docs.python.org/3/library/configparser.html
import requests #https://developers.virustotal.com/v2.0/reference#file-scan
import json

def abuseipdb(sessionpeer, mailfrom, mailto):
    config = configparser.ConfigParser()
    config.read('icarus.config')
    abuseip = config['IPDBAPI']['AbuseIPDB']
    apikey = config['IPDBAPI']['IPDBAPI']
    
    headers = { 'Key': apikey,   'Accept': 'application/json', }
    data = {'categories': '18,22'}


    if abuseip != "no":
        url = "https://api.abuseipdb.com/api/v2/report"

    
        if apikey == "PUT API KEY HERE":
            print ("This is your currently configured APIKEY in smtp.config:\n" + config['IPDBAPI']['IPDBAPI'])
        else:
            abusepost = requests.post('https://api.abuseipdb.com/api/v2/report', headers=headers, data=data)
            
           # requests.post(url, data={'ip': sessionpeer, 'comment': 'SMTP honeypot', 'Key': apikey, 'categories': '11', 'Accept': 'application/json'})
            print (abusepost)
            if abusepost.status_code != 200:
                print ("HTTP code isn't 200")


