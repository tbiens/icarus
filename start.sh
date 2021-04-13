#!/bin/bash
clear

if ! command -v tmux &> /dev/null
then
  echo 'Error: Tmux and Docker must be installed'
  exit
fi

if ! command -v docker &> /dev/null
then
  echo 'Error: Tmux and Docker must be installed'
  exit
fi

docker build -t icarus .
tmux -c 'docker run -a stdin -a stdout -it \
-p 21:2021/tcp -p 22:2022/tcp -p 23:2023/tcp \
-p 25:2025/tcp -p 110:20110/tcp -p 111:20111/tcp \
-p 135:20135/tcp -p 139:20139/tcp -p 143:20143/tcp \
-p 161:20161/udp -p 445:20445/tcp -p 1433:1433/tcp \
-p 1723:1723/tcp -p 3306:3306/tcp -p 3389:3389/tcp \
-p 5600:5600/udp -p 5900:5900/tcp  icarus'
