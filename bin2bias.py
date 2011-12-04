#!/usr/bin/python
import sys, argparse

#parser = argparse.ArgumentParser(description='Analyze bitwise bias of \
#binary data', epilog="Input is binary data for analysis. Output is lines \
#with place in file on vertical axis like this: #0 #1 %0 %1")
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
	counts = [0, 0]
	for byte in chunk:
#		bits = bin(byte)[2:]
#		for bit in "0"*(8-len(bits))+bits:
#			counts[int(bit)] += 1
		for bit in [int(bool(byte & x)) for x in [0x80, 0x40, 0x20, 0x10, 0x8, 0x4, 0x2, 0x1]]:
			counts[int(bit)] += 1
	p0 = counts[0]/sum(counts)
	p1 = counts[1]/sum(counts)
	print('%d %d %f %f' % (counts[0], counts[1], p0, p1))
