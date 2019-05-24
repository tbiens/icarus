# Icarus
**Goal:**

SMTP honeypot for collecting malware and automatically uploading to virustotal and report spammers to abuseipdb

There are many awesome SMTP honeypots but they are for spam. https://github.com/paralax/awesome-honeypots

**Future Features:**

1. Improve my skills significantly in Git and Python.
2. More than 1 attachment at a time.
3. Cleanup process for logs and downloads.
4. Cuckoo API?
5. Config file the IP choice.
6. Chroot or nobody:nobody.

**Docker**

git clone https://github.com/tbiens/icarus.git
nano icarus.config #change this config with your API keys
docker build -t icarus .
docker run -a stdin -a stdout -it -p 127.0.0.1:25:25/tcp icarus # change 127.0.0.1 to your ip. 
 

**Raspbian from scratch:**
Raspbian 9 has Python 3.5.3 by default. Which should work.

git clone https://github.com/tbiens/icarus.git

cd icarus

pip3 install --upgrade pip

pip3 install requests aiosmtpd

nano icarus.config  #Enter your virustotal API Key in.

python3 setup.py

**Debian 9 fresh install:**

apt-get update;apt-get dist-upgrade

apt-get install python3-pip git

pip3 install --upgrade pip

pip3 install requests aiosmtpd # if you get some wierd 'main' error. Just reboot.

git clone https://github.com/tbiens/icarus.git

cd icarus

nano icarus.config  #Enter your virustotal API Key in.

python3 setup.py


**Setup:**

Minimum Python seems to be 3.5 because of async and aiosmtpd. I made this in 3.7. 

**To run it:**

python3 setup.py

A copy of the attachments are kept in the ./downloads/ folder.

The virustotal links are stored in ./logs/virustotal.log
