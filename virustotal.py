import requests #https://developers.virustotal.com/v2.0/reference#file-scan
import json
import logging #https://docs.python.org/3.7/howto/logging.html
import configparser

logging.basicConfig(filename='logs/virustotal.log',level=logging.WARNING)


def virustotalfile(filename):
    
    config = configparser.ConfigParser()
    config.read('icarus.config')
    apikey = config['APIKEY']['apikey']
    URL_BASE = "https://www.virustotal.com/vtapi/v2/"
    url = URL_BASE + "file/scan"
    #This is just straight from virustotal link above
    
    attr = {"apikey": apikey}
    files = {"file": open("downloads/" + filename, 'rb')}
    viruspost = requests.post(url, data=attr, files=files)
    #pretty much just the API

    if apikey == "PUT API KEY HERE":
        print ("This is your currently configured APIKEY in smtp.config:\n" + config['APIKEY']['apikey'])
    else:

        if viruspost.status_code == 200:
            request = json.loads(viruspost.text)#The code on the virustotal page is python2, this was a pain to figure out for python3
            print(request["verbose_msg"])#especially difficult when I didn't know there would be code differences between 2 and 3.
            logging.warning(request["permalink"])#yaay debugging
            print (request["permalink"]) 
        else:
            print ("HTTP code isn't 200")
