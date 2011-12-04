#include <stdio.h>
#include <stdlib.h>

int readblock(long blocksize, char* buf){
	//will return 1 when the block has not been filled
	//unfilled blocks (the last one, usually) are ignored
	//returns 0 on a successfully filled block
	int i=0;
	int in=0;
	for (i=0; i<blocksize; i++) {
		in = getchar();
		if (in == EOF) return(1);
		buf[i] = in;
	}
	return(0);
}

char partbyte = 0;
char numbits = 0;

void buildbyte(char in_bit) {
	//in_bit should be 0 or 1
	partbyte = (partbyte << 1) + in_bit;
	numbits = (numbits + 1) % 8;
	if (numbits == 0){
		putchar(partbyte);
	}
}
