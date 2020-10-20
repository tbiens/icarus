FROM python:3.8-buster

RUN groupadd -r NOTROOT && useradd --no-log-init -r -g NOTROOT NOTROOT

WORKDIR /icarus

# Update aptitude with new repo
RUN apt-get update

# Install software
RUN apt-get install -y python3-pip screen nano

COPY requirements.txt .

#RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

#RUN git clone https://github.com/tbiens/icarus.git

RUN mkdir /icarus/logs

RUN mkdir /icarus/downloads

RUN touch /icarus/logs/virustotal.log

# config copy

COPY app/ ./app/

COPY setup.py .

COPY icarus.config /icarus/

RUN chown NOTROOT -R /icarus/

# running command

USER NOTROOT

CMD [ "python3", "/icarus/setup.py" ]
