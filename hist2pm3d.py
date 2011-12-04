#!/usr/bin/python
import sys

#input should be space-separated lines of
#waterfall-like quantites
#with time on the vertical axis
#types on horizontal axis
#bar heights as values

linecnt = 0

while 1:
	line = sys.stdin.readline()
	if len(line) == 0:
		break
	colcnt  = 0
	for col in line.split():
		print('%d %d %d' % (linecnt, colcnt, float(col)))
		colcnt += 1
	print()
	linecnt += 1
