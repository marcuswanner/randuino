#!/usr/bin/python

import sys

global partbit, numbits
partbit = 0
numbits = 0

def buildbyte(bit_in):
    global partbit, numbits
    partbit = (partbit << 1) + bit_in
    numbits = (numbits + 1) % 8
    #print("BIT_IN", bit_in, file=sys.stderr)
    if numbits == 0:
        #this weird line stops stdout from unicoding the bytes
        sys.stdout.write(bytes(chr(partbit), "latin-1"))
        partbit = 0 

global curbyte, bitsleft
curbyte = 0
bitsleft = 0

def nextbit():
    global curbyte, bitsleft
    if not bitsleft:
        curbyte = sys.stdin.read(1)
        if not curbyte: return -1
        curbyte = ord(curbyte)
        bitsleft = 8
    #print(curbyte, file=sys.stderr)
    ret = int((curbyte&0x80)>0)
    curbyte = (curbyte<<1) & 0xff
    bitsleft -= 1
    return ret

sys.stdout = sys.stdout.detach()
sys.stdin = sys.stdin.detach()

while 1:
    inbits = [nextbit(), nextbit()]
    #print(inbits, file=sys.stderr)
    if -1 in inbits: break
    if inbits[0] != inbits[1]:
        buildbyte(inbits[0])

