#!/bin/bash
git pull origin mj
nc -nl -p 9000 -e update.sh
