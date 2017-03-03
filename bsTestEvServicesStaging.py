#!/usr/bin/env python
import shlex, subprocess
import socket
import os
import time
from time import sleep
from subprocess import call, Popen, check_output, PIPE
from nbstreamreader import NonBlockingStreamReader as NBSR
import signal

def sig_handler(sig, frame):
    print "got sig(sig)\n"
    safe_exit(sig)
    
signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)

def make_calls (cmdline,count,agents,dial):
    print "cycling(count)\n"
    for i in range(count):
        who = dial[i % len(dial)]
        call = "d"+who+"\n"
        print call
        cmdline.write(call)
        sleep (0.1)
        cmdline.write("T")

def test_event_server (cmdline,count,agents,dial):
    print "cycling(count)\n"
    for i in range(count):
        who = dial[i % len(dial)]
        cmdline.write("b")
        sleep (0.1)
        call = "d"+who+"\n"
        print call
        cmdline.write(call)
        sleep (3)
        cmdline.write("T")

def safe_exit(level):
    global cmdline
    global calls
    global process
    # save stuff
    print("Exiting ...\n")
    cleanup(calls, cmdline)
    exit(0)

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

    make_calls(cmdline,count,agents,dial)
    timeout = time.time()
    timeoutStarted = True
    while (True):
        test_event_server(cmdline,count,agents,dial)
        if (time.time() > (timeout + TIMEOUT_SECONDS)):
            print "timeout\n", timeout, time.time()
            cleanup(count,cmdline)
            break

calls = 144
print "dialing - ", calls, "calls\n"
dials = ("55560", "3000", "3001", "70062", "4703","67892","4701","713300")
#dials = ("8600",)
agents = 2;
#agents = 1;
print dials
port = '5565'
#port = '5555'
args = shlex.split('/bin/netcat -u 127.0.0.1 ' + port)
p = Popen(args, stdin=PIPE, stdout=PIPE,stderr=PIPE, shell=False)
nbsr = NBSR(p.stdout)
cmdline=p.stdin

testing(calls,agents,dials)
sleep(10)
cleanup(calls,cmdline)
