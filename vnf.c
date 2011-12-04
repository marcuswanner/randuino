#include <stdio.h>
#include <stdlib.h>
#include "common.c"

unsigned char curbyte = 0;
char bitsleft = 0;

char nextbit() {
	//returns 0 or 1
	//<0 for error
	if (bitsleft == 0) {
		int in=getchar();
		if (in == EOF) return(-1);
		curbyte = in;
		bitsleft = 8;
	}
	//printf("curbtye: %hhu\n", curbyte);
	char ret = (curbyte&0x80)>0;
	curbyte<<=1;
	bitsleft--;
	return ret;
}

int main() {
	char inbits[2] = {0, 0};
	while ((inbits[0]=nextbit())>=0 && (inbits[1]=nextbit())>=0) {
		//core of the von neumann filter
		//printf("inbits: %hhd%hhd\n", inbits[0], inbits[1]);
		if (inbits[0] == inbits[1]) continue;
		else buildbyte(inbits[0]);
	}
	return(0);
}
