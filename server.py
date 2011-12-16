#!/usr/bin/python
import sys, subprocess
from queue import Queue
from threading import Thread, Lock
from time import sleep

#basically an application-wide buffer size
#this many bytes are handled at a time
#up to this many bytes may be dropped when using tap()
#and directing it to not copy the data (the default)
BLOCKSIZE=128


tostr = lambda byte: str(byte, 'latin-1')
tobytes = lambda string: bytes(string, 'latin-1')
def totype(indata, targettype):
    if type(indata) == targettype: return indata
    if targettype == str:       return tostr(indata)
    elif targettype == bytes:   return tobytes(indata)

def run(command):
    "takes command and arguments in a list"
    "returns stdout and stdin file objects"
    p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return(p.stdout, p.stdin, p)


class StreamNode():
    "A running command which is a piece of the data pipe"
    def __init__(self, command, types):
        self.stdout, self.stdin, self.p = run(command)
        self.outtype, self.intype = types
    
    def stop():
        self.p.kill()

class EndNode():
    "A file which is only written to and forms the end of a pipe"
    def __init__(self, infile, datatype=str):
        self.stdout, self.stdin = None, infile
        self.outtype, self.intype = None, datatype 
        self.p = None
    
    def stop():
        pass

class SourceNode():
    "A file which is only read from and forms the beginning of the pipe"
    def __init__(self, outfile, datatype=str):
        self.stdout, self.stdin = outfile, None
        self.outtype, self.intype = datatype, None
        self.p = None
    
    def stop():
        pass


class SplitThread(Thread):
    "grabs input from an infile and duplicates it across one or more outs"
    "can be tapped in both yank and del modes"
    "file descriptors used by this class must be in BINARY MODE"
    def init(self, infile, outfiles, name=None):
        self.setDaemon(True)
        self.infile, self.outfiles = infile, outfiles
        self.tapreqs = Queue()
        self.name = name
        self.debug = False

    def tap(self, n, copy=False):
        "grab n bytes from the running pipe"
        "if copy is False, the bytes returned (plus enough to make an even"
        "block) will be removed from the pipe and never seen by outfiles"
        "returns bytes"
        "this method SHOULD be threadsafe"
        "name is used for identifying when we error out"
        nblocks = n//BLOCKSIZE+1
        blocks = []
        for bid in range(nblocks):
            q = Queue()
            self.tapreqs.put([copy, q])
            blocks.append(q.get())
        return b''.join([totype(b, bytes) for b in blocks])[:n]
    
    def addout(self, out):
        "add an out to the splitter using this method"
        "argument is in standard format of [fdesc, type]"
        "to remove an out, simply close the file descriptor"
        self.outfiles.append(out)

    def run(self):
        while 1:
            try:
                block = self.infile.read(BLOCKSIZE)
                if len(block) < BLOCKSIZE:
                    raise IOError("Block not filled")
            except:
                #what do we do now? the command exited, probably
                #in any case, we can't go on
                #TODO: investigate what happens to downstream stuff
                print("SplitThread's infile died (name=%s)" % self.name)
                print(sys.exc_info())
                for out in self.outfiles:
                    out[0].close()
                break
            if self.tapreqs.qsize():
                copy, cbq = self.tapreqs.get()
                cbq.put(block)
                if self.debug:
                    print("SplitThread %s giving block to tap" % self.name)
                if not copy:
                    continue
            if self.debug:
                print("SplitThread %s sending block to outfiles" % self.name)
            for out in self.outfiles:
                try:
                    out[0].write(totype(block, out[1]))
                    out[0].flush()
                except:
                    print("Removing outfile from SplitThread (name=%s):" % self.name)
                    print(sys.exc_info())
                    self.outfiles.remove(out)

def linknodes(innode, outnodes, name):
    infile = innode.stdout
    outfiles = []
    for node in outnodes:
        outfiles.append([node.stdin, node.intype])
    splitter = SplitThread()
    splitter.init(infile, outfiles, name)
    splitter.start()
    return splitter 

def addnode(splitter, outnode):
    splitter.addout([node.stdin, node.intype])


if __name__ == "__main__":
    #dumpn = StreamNode(['cat', '/dev/urandom'], [bytes, None])
    dumpn = StreamNode(['./dump.py', str(BLOCKSIZE)], [bytes, None])
    #dumpn = SourceNode(open('server.py', 'r'))
    #hexn = StreamNode(['hexdump', '-C'], [bytes, bytes])
    vnfn = StreamNode('./vnf', [bytes, bytes])
    #printn = EndNode(sys.stdout)
    dumps = linknodes(dumpn, [vnfn], "dump")
    dumps.debug = True
    vnfs = linknodes(vnfn, [], "vnf")
    vnfs.debug = True
    #hexs = linknodes(hexn, [printn], "hex > print")
    while 1:
        sleep(1)
        print("dumps", dumps.tap(100, True))
        print("vnfs", vnfs.tap(100, True))
        #i = dumps.tap(100, False)
        #this makes a mess
        #print(i)


