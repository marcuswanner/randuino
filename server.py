#!/usr/bin/python
import sys, subprocess
from queue import Queue
from threading import Thread, Lock
from time import sleep

#basically an application-wide buffer size
BLOCKSIZE=128

def tostr(bytearray): return
tostr = lambda ba: str(ba, 'latin-1')
tobytes = lambda string: bytes(string, 'latin-1')

def run(command):
    "takes command and arguments in a list"
    "returns stdout and stdin file objects"
    p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return(p.stdout, p.stdin)

class SplitThread(Thread):
    "grabs input from an infile and duplicates it across one or more outs"
    "can be tapped in both yank and del modes"
    "file descriptors used by this class must be in BINARY MODE"
    def init(self, infile, outfiles):
        self.setDaemon(True)
        self.infile, self.outfiles = infile, outfiles
        self.tapreqs = Queue()
        self.tapblocks = Queue()
        self.tapwaiting = Lock()

    def tap(self, n, copy=False):
        "grab n bytes from the running pipe"
        "if copy is False, the bytes returned (plus enough to make an even"
        "block) will be removed from the pipe and never seen by outfiles"
        "returns a STRING!"
        nblocks = n//BLOCKSIZE+1
        blocks = []
        for bid in range(nblocks):
            q = Queue()
            self.tapreqs.put([copy, q])
            blocks.append(q.get())
        return ''.join([tostr(b) for b in blocks])[:n]
    
    def run(self):
        while 1:
            sleep(0.2)
            block = self.infile.read(BLOCKSIZE)
            if len(block) < BLOCKSIZE:
                break
            if self.tapreqs.qsize():
                copy, cbq = self.tapreqs.get()
                cbq.put(block)
                if not copy:
                    continue
            for out in self.outfiles:
                out.write(block)
                out.flush()

if __name__ == "__main__":
#    dumpout, dumpin = run('./dump.py')
    dumpout, dumpin = run(['cat','testfile'])
    hexout, hexin = run('hexdump')
    testfileout = open('testfileout', 'wb')
    bitbucket = open('/dev/null', 'w')
    dump = SplitThread()
    dump.init(dumpout, [testfileout])
    dump.start()
    while 1:
        sleep(1)
        print(dump.tap(200, False))
        sleep(1)
        print(dump.tap(200, True))


