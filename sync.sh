#!/bin/sh
wget -q --spider http://google.com

if [ $? -eq 0 ]; then
	cd ~/ArduinoRaspberryTempLogger
	git add *.csv
	git commit -m "arduino sensor data"
	git push
fi
