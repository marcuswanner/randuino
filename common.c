#include <stdio.h>
#include <stdlib.h>

int readblock(long blocksize, char* buf){
	//will return 1 when the block has not been filled
	//unfilled blocks (the last one, usually) are ignored
	//returns 0 on a successfully filled block
	int i=0;
	char tmp=0;
	for (i=0; i<blocksize; i++) {
		//printf("%d\n", i);
		if ((buf[i] = getchar()) == EOF) {
			return(1);
		}
	}
	return(0);
}
