#!/bin/bash
git fetch origin mj
git reset --hard origin/mj
nc -nl -p 9000 -e update.sh &
