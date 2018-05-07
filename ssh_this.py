#!/usr/bin/env python3
#ident $Id$ $Date$

from multiprocessing import Process, Pipe, current_process
from threading import Thread
from subprocess import check_output, Popen, PIPE, TimeoutExpired
import sys, shlex
from time import sleep
import signal
resources=[]

def safe_exit():
    counter=1
    for r in resources:
        print ("deleting {}\n".format(counter))
        del r
        counter +=1
    exit(0)

'''
ls -l mserver logs:
ssh xcast@logserver3-la.siptalk.com 'ls -l logs/servers/container1-la.xcastlabs.net/20180522/mserver*.node*.log | grep -v 'job-''
ssh xcast@logserver3-la.siptalk.com 'ls -l logs/servers/container2-la.xcastlabs.net/20180522/mserver*.node*.log | grep -v 'job-''


def my_printer(r):
    try:
        if not r:
            print("There is no Input")
            exit(-1)
        print("VERBOSE printer")
        while r:
            record=r.recv()
            if(record):
                print("got something")#record.decode('UTF-8').strip())
    except Exception as inst:
        print (type(inst))
        print (inst.args)
        print (inst)
        print (__file__, 'Oops')
'''
def main(argv):
    #print(argv[0])
    #exit(0)
    #r, w = Pipe(duplex=False)
    #printer = Process(target=my_printer, args=(r,))
    #resources.append(printer)
    #printer.start()
    #print(argv)
    args = ['/usr/bin/ssh', argv[0]]
    #print(" ".join(args))
    params=" ".join(argv[1:]).encode()
    #print(params)
    #exit(0)
    proc = Popen(args, stdin=PIPE, stdout=PIPE,stderr=PIPE, shell=False)
    #sleep(3)
    #proc.kill()
    #exit(0)
    try:
        outs, errs = proc.communicate(input=params,timeout=15)
        print(outs.decode('UTF-8').strip())
    except TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
    except Exception as inst:
        print (type(inst))
        print (inst.args)
        print (inst)
        print (__file__, 'Oops')

if __name__ == "__main__":
   main(sys.argv[1:])
