"""virustotal module for uploading samples"""

import json
import logging  # https://docs.python.org/3.7/howto/logging.html
from app.config import config
import requests  # https://developers.virustotal.com/v2.0/reference#file-scan

logging.basicConfig(filename='logs/virustotal.log', level=logging.WARNING)


def virustotalfile(filename):
    """uploads the file to api"""
    url_base = "https://www.virustotal.com/vtapi/v2/"
    url = url_base + "file/scan"
    # This is just straight from virustotal link above

    attr = {"apikey": config.vtapikey}
    with open("downloads/" + filename, 'rb') as vtfile:
        files = {"file": vtfile}
        viruspost = requests.post(url, data=attr, files=files)
        # pretty much just the API
        if config.virustotal != 'no':  # virustotal disabled by default.
            if config.vtapikey != "PUT API KEY HERE":
                if viruspost.status_code == 200:
                    request = json.loads(viruspost.text)
                    logging.warning(request["permalink"])
