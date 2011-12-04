#include <stdio.h>
#include <stdlib.h>

//for values 0-1023, this should be fine at 5
#define MAXLINELENGTH 10

int readline(char* buf) {
	int i=0;
	int in=0;
	for (i=0; i<MAXLINELENGTH; i++) {
		in = getchar();
		if (in == EOF) return(1);
		if (in == '\n') {
			buf[i] = 0;
			return(0);
		}
		buf[i] = in;
	}
	//if we get to here, we exceeded MAXLINELENGTH
	return(2);
}

char partbyte = 0;
char numbits = 0;

void buildbyte(char in_bit) {
	//in_bit should be 0 or 1
	//printf("numbits: %hhd\n", numbits);
	partbyte = (partbyte << 1) + in_bit;
	numbits = (numbits + 1) % 8;
	if (numbits == 0){
		putchar(partbyte);
	}
}

int main() {
	char buf[MAXLINELENGTH];
	while (readline(buf) == 0) {
		//printf("%s\n", buf);
		buildbyte(atoi(buf)%2);
	}
	return(0);
}
