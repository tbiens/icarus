#!/bin/bash
clear
#cd /icarus
#docker build --no-cache -t icarus .
docker build -t icarus .
screen docker run -a stdin -a stdout -it -p 21:21/tcp -p 22:22/tcp -p 23:23/tcp -p 25:25/tcp -p 110:110/tcp -p 111:111/tcp -p 135:135/tcp -p 139:139/tcp -p 143:143/tcp -p 161:161/udp -p 445:445/tcp -p 1433:1433/tcp -p 1723:1723/tcp -p 3306:3306/tcp -p 3389:3389/tcp -p 5600:5600/udp -p 5900:5900/tcp  icarus
