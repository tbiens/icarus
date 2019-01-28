# Icarus
**Goal:**

SMTP honeypot for collecting malware and automatically uploading to virustotal.

There are many awesome SMTP honeypots but they are for spam. https://github.com/paralax/awesome-honeypots

**Future Features:**

1. Log to ELK or Splunk

3. Report IP addresses to an antispam api service.
4. Improve my skills significantly in Git and Python. 
5. More than 1 attachment at a time.

7. Cleanup process for logs and downloads.
8. Cuckoo API?
9. Config file the IP choice.
10. Chroot or nobody:nobody.

**Raspbian from scratch:**
Raspbian 9 has Python 3.5.3 by default. Which should work.

git clone https://github.com/tbiens/icarus.git

cd icarus

pip3 install --upgrade pip

pip3 install requests aiosmtpd

python3 setup.py


**Setup:**

Minimum Python seems to be 3.5 because of async and aiosmtpd. I made this in 3.7. 

apt-get install python3-requests python3-aiosmtpd

or
>#Python3 requests module is for uploading to virus total; aiosmtpd for the smtp protocol.

pip3 install requests aiosmtpd 

>#Enter your virustotal API Key in.

nano icarus.config  

**To run it:**

python3 setup.py

A copy of the attachments are kept in the ./downloads/ folder.

The virustotal links are stored in ./logs/virustotal.log
