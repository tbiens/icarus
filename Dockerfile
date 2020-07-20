FROM python:3.8

WORKDIR /icarus

# Update aptitude with new repo
#RUN apt-get update && apt-get dist-upgrade -y

# Install software
#RUN apt-get install -y git python3-pip python-virtualenv screen nano

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

#RUN git clone https://github.com/tbiens/icarus.git

RUN touch /icarus/logs/virustotal.log

# config copy

COPY app/ .

COPY icarus.config /icarus/

# running command

CMD [ "python3", "/icarus/setup.py" ]
