#!/usr/bin/python2
import serial, sys

stdout = sys.stdout

s = serial.Serial('/dev/ttyUSB0', 19200)

while 1:
	buf = s.read(4096)
	if not buf:
		break
	stdout.write(buf)
