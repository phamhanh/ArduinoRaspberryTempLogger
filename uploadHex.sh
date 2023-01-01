#!/bin/sh
sudo killall --user brewpi
avrdude -c arduino -p atmega328p -P /dev/ttyACM0 -b 115200 -U flash:w:brewpi.hex:i
