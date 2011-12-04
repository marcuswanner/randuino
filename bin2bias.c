#include <stdio.h>
#include <stdlib.h>
#include "common.c"

void checkblock(long blocksize, char* buf) {
	int cid=0;
	int mask=0;
	char comp=1;
	long counts[2] = {0, 0};
	for (cid=0; cid<blocksize; cid++) {
		for (mask=1; mask<=128; mask=mask << 1) {
			if ((buf[cid]&mask)>0) { counts[1]++; }
			else { counts[0]++; }
		}
	}
	double sum = counts[0] + counts[1];
	float p0 = counts[0]/sum;
	float p1 = counts[1]/sum;
	printf("%ld %ld %f %f\n", counts[0], counts[1], p0, p1);
}

int main(int argc, char *argv[]) {
	int i = 0; //currently unused
	long blocksize = 4096;
	if (argc > 1) {
		blocksize = atol(argv[1]);
	}
	//printf("BS: %d\n", blocksize);
	char* buf = malloc(blocksize);
	while (readblock(blocksize, buf) == 0) {
		checkblock(blocksize, buf);
	}
	free(buf);
	return(0);
}

