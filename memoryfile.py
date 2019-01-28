import io #https://docs.python.org/3/library/allos.html
#import shutil
import os #for os.path.isfile
import hashlib #https://docs.python.org/3/library/hashlib.html
#import sqlite3 #https://docs.python.org/3/library/sqlite3.html
from virustotal import virustotalfile #Check out virustotal.py
from datetime import datetime


def inmemoryfile(filecontents):
    memoryfile = io.StringIO()
    memoryfile.write(filecontents)
    #This stores the file in memory. We limit email size to 30MB or so.
    email = memoryfile.getvalue()
    if 'Content-Disposition: attachment;' in filecontents: #Checking if there's an attachment
        beforeboundary = email.split('Content-Disposition: attachment;')[1]

        #emails have a bunch of stuff in it, I'm splitting the attachment off.
        attachment = beforeboundary.split('--boundary')[0]
   
    #there was a tiny bit of text after the attachment that was screwing up the sha256
        shahash = hashlib.sha256(attachment.encode()).hexdigest() # read() the file, then you need to convert it to bytes with encode, then hexdigest cleans up
        if os.path.isfile("./downloads/" + shahash):
            print("Already have this attachment") #checking if I have already received that file
        else:
            filename = open("downloads/" + shahash,"w+") # open sha256 named file
            filename.write(attachment) #Reading the memoryfile into the actual file being written to disk.
            filename.close() #closing is important.
            virustotalfile(shahash) #Send the file to my virustotal script
            memoryfile.close() #closing is important.
    
    else:
        print("No attachment?")
  

def loggingaddresses(sessionpeer, mailfrom, mailto): #Logging connections to a csv file
    
    nowdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #What date and time.
    loggingfile = open("logs/logging.csv","a+")
    #Opening logs/logging.csv in append mode. 
    loggingfile.write(sessionpeer + "," + mailfrom + "," + mailto + "," + str(nowdate) + "\n")
    #Logging, IP, From, To, and the Date
    loggingfile.close()
    

    