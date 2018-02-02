#!/usr/bin/env python
import shlex, time
from subprocess import call, Popen, check_output, PIPE
from Queue import Queue, Empty
#from nbstreamreader import NonBlockingStreamReader as NBSR
from multiprocessing import Process, Pipe, current_process

#connect_cmd="ssh ndarmoni@bdsupportdb-02.siptalk.com /home/ndarmoni/bin/clicking.py"
connect_cmd="ssh ndarmoni@bdsupportdb-02.siptalk.com /home/ndarmoni/bin/monitor_me"
#ls_cmd="pwd; 'ls -l ./bin';  'cat ./bin/*\n'"
#args=shlex.split(connect_cmd + " " + ls_cmd)
#print (args)
#print (repr(check_output(args)))

#PORT = 32802
#sock = socket(AF_INET,SOCK_DGRAM)
#msg = "show talbes;"
#for counter in range(3):
#    sock.sendto(msg.encode('utf-8'),('38.102.250.167', PORT))
def logger(sin):
    while True:
        try:
            msg = sin.recv()
        except EOFError:
            time.sleep(3)
            continue    
        else:
            if(msg):
                print(msg)

r, w = Pipe(duplex=False)
args = shlex.split(connect_cmd)#/home/ndarmoni/bin/monitor_me
#print (args)
p = Popen(args, stdin=PIPE, stdout=w,stderr=PIPE, shell=False, bufsize=0)
#print(p)
log = Process(target=logger, args=(r,))
log.start()

# wrap p.stdout with a NonBlockingStreamReader object:
if( p ):
    #p.stdout.close()
    try:
        for c in range(0,190):
            p.stdin.write("show talbes;")
        time.sleep(2)
        #error = p.stderr.readlines()
        #print >>sys.stderr, "ERROR: %s" % error
        while True:
            time.sleep(3)

    except Exception as inst:
            type(inst)
            print(inst.args)
            print(inst)
            print(__file__, 'Oops')
else:
    print("p is not...")

