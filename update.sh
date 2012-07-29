#!/bin/bash
cd /home/ubuntu/ws/
git fetch
git reset origin/mj
nc -nl -p 9000 -e update.sh &
