#!/bin/bash
git fetch
git reset --hard origin/mj
nc -nl -p 9000 -e update.sh &
