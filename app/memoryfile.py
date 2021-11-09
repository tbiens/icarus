"""creates files that are stored entirely in memory"""

import io  # https://docs.python.org/3/library/allos.html
import os  # for os.path.isfile
import hashlib  # https://docs.python.org/3/library/hashlib.html
from app.virustotal import virustotalfile  # Check out virustotal.py
import app.cfg


def lastattacker(ipaddr):
    """keeps track of the last 5 unique attackers."""
    app.cfg.numattacks['num'] = app.cfg.numattacks['num'] + 1
    # Last 5 reports.
    if ipaddr in app.cfg.attackers:
        pass
    else:
        if len(app.cfg.attackers) > 4:
            del app.cfg.attackers[-1]
        app.cfg.attackers.insert(0, ipaddr)


def inmemoryfile(filecontents):
    """ io.Stringio is a file stored in memory."""
    memoryfile = io.StringIO()
    memoryfile.write(filecontents)
    # This stores the file in memory. We limit email size to 30MB or so.
    email = memoryfile.getvalue()

    # Checking if there's an attachment
    if 'Content-Disposition: attachment;' in filecontents:
        beforeboundary = email.split('Content-Disposition: attachment;')[1]

        # emails have a bunch of stuff in it, I'm splitting the attachment off.
        attachment = beforeboundary.split('--boundary')[0]

        # there was a tiny bit of text after the attachment that was screwing up the sha256
        shahash = hashlib.sha256(attachment.encode()).hexdigest()
        # read() the file, then you need to convert it to bytes with encode, then hexdigest cleans up
        if os.path.isfile("./downloads/" + shahash):
            print("Already have this attachment")  # checking if I have already received that file
        else:
            with open("downloads/" + shahash, "w+", encoding="utf8") as filename:  # open sha256 named file
                filename.write(attachment)  # Reading the memoryfile into the actual file being written to disk.
            filename.close()  # closing is important.
            virustotalfile(shahash)  # Send the file to my virustotal script
            memoryfile.close()  # closing is important.
