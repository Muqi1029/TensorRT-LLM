#!/bin/bash

pkill -f "python3 ./register.py"

python3 ./starter/check_pre_stop.py > /dev/stdout 2>&1
