#!/usr/local/opt/python/libexec/bin/python

'''
to use python 2 use /usr/bin/python2
requires pySerial to be installed
add date to the header, and time to the begining of each line
add sys argument to customize
USE: make executable by chmod +x scriptname.py and
> ./recordSerial.py test1000.txt (and Enter)
'''

import serial, time, sys
import os, errno



print("Press Ctrl+C to save and stop the logging")
baud_rate = 9600  #  In arduino, Serial.begin(baud_rate), e.g. 115200
default = time.strftime("temp_%Y%m%d_%H%M.csv")
default_link = "temp.csv"
#serial_port = '/dev/tty.usbserial-14330'  #  listening port, type ls /dev/ttyUSB* in shell for available ports
serial_port = '/dev/ttyUSB0'  #  listening port, type ls /dev/ttyUSB* in shell for available ports
if len(sys.argv) == 2:
    logfile_name = sys.argv[1]
else:
    logfile_name = default

os.remove(default_link)
os.symlink(logfile_name, default_link)

output_file = open(logfile_name, "a+")
#output_file.write(time.strftime("%x\n"))
ser = serial.Serial(serial_port, baud_rate)
count = 0

try:
    while True:
        line = ser.readline();
        line = line.decode("utf-8")  #  ser.readline returns a binary, convert to string
        timeNow = time.strftime("%X")
        #outputline = ",".join((timeNow, line))
        if line != "\n":            #  not record an empty line
            print(timeNow, line)
            output_file.write(line)
            count +=1
        else:
            continue
            #  print("\nnothing here")
        if count >= 1:             #  to save file to disk every 1 lines
            output_file.close()
            output_file = open(logfile_name, "a+")
            count = 0
except KeyboardInterrupt:
    print(">> Ctrl+C pressed, stop logging to {} file".format(logfile_name))
    output_file.close()
    raise SystemExit
