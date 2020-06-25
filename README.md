# Icarus
**Goal:**

SMTP, SNMP, SMB honeypot for collecting malware and automatically uploading to virustotal and report abusive IPs to abuseipdb. 

There are many awesome honeypots. https://github.com/paralax/awesome-honeypots

**Features:**




**Future Features:**

1. Keep 1 day of ip addresses and only report once a day.
2. More than 1 attachment at a time.
3. SMB accept files to upload to virustotal
4. Increase protocol interaction.
5. Dynamically allow any number of ports via config.


**Docker**

git clone https://github.com/tbiens/icarus.git

nano icarus.config #change this config with your API keys

docker build --no-cache -t icarus .

docker run -a stdin -a stdout -it -p 21:21/tcp -p 22:22/tcp -p 23:23/tcp -p 25:25/tcp -p 5900:5900/tcp -p 161:161/udp -p 445:445/tcp -p 5600:5600/udp -p 1433:1433/tcp icarus
 
