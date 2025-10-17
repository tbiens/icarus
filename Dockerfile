FROM python:3.10-slim-bullseye

RUN groupadd -r NOTROOT && useradd --no-log-init -r -g NOTROOT NOTROOT

WORKDIR /icarus

# Install software
RUN apt-get update && apt-get install -y screen nano

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
