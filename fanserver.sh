#!/bin/bash
# put in /etc/rcS.d/
cd ~/fan_server
pigpiod
python webserver.py &
./ngrok http 80 &
echo "fan server started check localhost:4040 for ngok url"
