#include <stdio.h>
#include <stdlib.h>
#include "common.c"

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

int main() {
	char buf[MAXLINELENGTH];
	while (readline(buf) == 0) {
		//printf("%s\n", buf);
		buildbyte(atoi(buf)%2);
	}
	return(0);
}
