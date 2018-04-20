#!/usr/bin/env python
import shlex, subprocess
import socket
import os
import time
from time import sleep
from subprocess import call, Popen, check_output, PIPE
from nbstreamreader import NonBlockingStreamReader as NBSR
import signal

global cmdline

def safe_exit(level):
    global cmdline
    print 'Killing Server'
    if not cmdline:
        exit(0)
    cmdline.write("q\n")
    sleep(0.1)
    cmdline.close()
    exit(0)

def sig_handler(sig, frame):
    print "got sig({})\n".format(sig)
    safe_exit(sig)

signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)

def make_calls (cmdline,count,agents,dial):
    print "calling({})\n".format(count)
    for i in range(count):
        who = dial[i % len(dial)]
        call = "d"+who+"\n"
        print call
        cmdline.write(call)
        sleep (7)
        if not cmdline:
            break
        if(1 < agents):
            cmdline.write("T\n")

def cleanup (calls, cmdline):
    global agents

#    if(is_numeric(calls)):
    print "Number of calls to close is " , calls, "\n"
    for a_calls in range(calls):
        cmdline.write("b")
        sleep(0.01)
        if(1 < agents):
            cmdline.write('T\n')

TIMEOUT_SECONDS = 2*60

def testing(count, agents, dial):
    global cmdline
    timeout = time.time()
    timeoutStarted = True

    while (True):
        make_calls(cmdline,count,agents,dial)
        if (time.time() > (timeout + TIMEOUT_SECONDS)):
            print "timeout\n", timeout, time.time()
            cleanup(count,cmdline)
            break
    cleanup(count,cmdline)

calls = 20
print "dialing - ", calls, "calls\n"
stars = ["*69", "*72", "*73", "*92", "*93", "*94", "*95", "*67", "*67", "*82", "*82", "*77", "*87", "*78", "*79", "*57", "*56", "*70", "*76", "*30", "*31", "*21", "*20"]
dials = stars +["*927161","*73","*727160","*73","*727161","*30", "*31", "*93","*947160","*95", "*947161"]
#dials = ("8600",)
#agents = 2;
agents = 3;
agents = 1;
print dials, agents
#exit(0)
port = '5565'
#port = '5555'
args = shlex.split('/bin/netcat -u 127.0.0.1 ' + port)
p = Popen(args, stdin=PIPE, stdout=PIPE,stderr=PIPE, shell=False)
nbsr = NBSR(p.stdout)
cmdline=p.stdin

testing(calls,agents,dials)
sleep(10)
cleanup(calls,cmdline)
