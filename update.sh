#!/bin/bash
cd /home/ubuntu/ws/
git fetch origin mj
git reset --hard origin/mj
git pull origin mj
nc -nl -p 9000 -e update.sh &
