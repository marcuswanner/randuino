#!/usr/bin/python
import sys, argparse

#parser = argparse.ArgumentParser(description='Analyze bitwise bias of \
#binary data', epilog="Input is binary data for freq analysis. Output is \
#space-separated lines of waterfall-like quantites with place in file on \
#vertical axis, byte values on horizontal axis, and popularity of each byte \
#as values.")
#parser.add_argument('-s', default=4096, dest='chunksize', type=int,
#                   help='size of each chuck to consider separately')
#chunksize = parser.parse_args().chunksize
try:
    chunksize = int(sys.argv[1])
except IndexError:
    chunksize = 4096

stdin = sys.stdin.detach()

while 1:
	chunk = stdin.read(chunksize)
	if len(chunk) < chunksize:
		break
	counts = {}
	for i in range(256): counts[i] = 0
	for byte in chunk:
		counts[byte] += 1
	for i in range(256):
		sys.stdout.write(' %d' % counts[i])
	print()
