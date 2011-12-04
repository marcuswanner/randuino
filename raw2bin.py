#!/usr/bin/python

import sys

stdin = sys.stdin
stdout = sys.stdout
partbit = 0
numbits = 0

while 1:
	line = stdin.readline()
	if not line: break
	bit_in = int(line) % 2
	#stdout.write(str(bit_in))
	partbit = (partbit << 1) + bit_in
	numbits = (numbits + 1) % 8
	if numbits == 0:
		sys.stdout.write(chr(partbit))
		#print(partbit)
		partbit = 0 
