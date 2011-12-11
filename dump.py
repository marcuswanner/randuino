#!/usr/bin/python2
import serial, sys

try:
    chunksize = int(sys.argv[1])
except IndexError:
    chunksize = 4096

stdout = sys.stdout

s = serial.Serial('/dev/ttyUSB0', 19200)

while 1:
	buf = s.read(chunksize)
	if not buf:
		break
	stdout.write(buf)
	stdout.flush()
