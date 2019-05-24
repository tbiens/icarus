FROM debian

# Update aptitude with new repo
RUN apt-get update

RUN apt-get dist-upgrade

# Install software
RUN apt-get install -y git python3-pip python-virtualenv

RUN pip3 install --upgrade pip

RUN pip3 install requests aiosmtpd

RUN git clone https://github.com/tbiens/icarus.git

RUN touch /icarus/logs/virustotal.log

# running command

CMD [ "python3", "/icarus/setup.py" ]