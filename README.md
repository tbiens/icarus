# Icarus
**Goal:**

Multiprotocol honeypot for collecting malware and automatically uploading to virustotal and report abusive IPs to abuseipdb. 

There are many awesome honeypots: https://github.com/paralax/awesome-honeypots

**Features:**

1. Accepts emails, processes attachments to send to virustotal.
2. Dynamically open any tcp or udp port as per config.
3. SMTP, SMB, and FTP are higher interaction.
4. Any connections to honeypot can be reported to abuseipdb.
5. Larg*Feed to build custom threat feed.


**Docker**

git clone https://github.com/tbiens/icarus.git

nano icarus.config #change this config with your API keys

bash start.sh