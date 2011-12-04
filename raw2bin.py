#!/usr/bin/python

import sys

sys.stdout = sys.stdout.detach()
partbit = 0
numbits = 0

while 1:
	line = sys.stdin.readline()
	if not line: break
	bit_in = int(line) % 2
	partbit = (partbit << 1) + bit_in
	numbits = (numbits + 1) % 8
	if numbits == 0:
		#this weird line stops stdout from unicoding the bytes
		sys.stdout.write(bytes(chr(partbit), "latin-1"))
		partbit = 0 
