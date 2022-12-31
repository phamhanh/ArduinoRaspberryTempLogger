#!/bin.sh
avrdude -c arduino -p atmega328p -P /dev/ttyACM0 -b 115200 -U flash:r:adduinoDownload.hex:i
