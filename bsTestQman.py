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
    print "got sig(", sig,")\n"
    safe_exit(sig)

signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)

def make_calls (cmdline,count,agents,dial):
    print "calling",count,"\n"
    for i in range(count):
        who = dial[i % len(dial)]
        call = "d"+who+"\n"
#        print call
        cmdline.write(call)
        sleep (0.1)
        cmdline.write("T")
        sleep (0.2)

def test_event_server (cmdline,count,agents,dial):
    print "cycling",count,"\n"
    for i in range(count):
        who = dial[i % len(dial)]
        cmdline.write("b")
        sleep (0.1)
        call = "d"+who+"\n"
#        print call
        cmdline.write(call)
        sleep (0.6)
        cmdline.write("T")
        sleep (0.4)

def safe_exit(level):
    global cmdline
    global calls
    global process
    global agents
    # save stuff
    print("Exiting ...\n")
    cleanup(calls+2*agents, cmdline)
    exit(0)

def cleanup (calls, cmdline):
    global agents

#    if(is_numeric(calls)):
    print "Number of calls to close is", calls, "\n"
    for a_calls in range(calls):
        cmdline.write("b")
        sleep(0.1)
        if(1 < agents):
            cmdline.write('T\n')

TIMEOUT_SECONDS = 0.4*60

def testing(count, agents, dial):
    global cmdline

    timeout = time.time()
    make_calls(cmdline,count,agents,dial)
    timeoutStarted = True
    while (True):
        test_event_server(cmdline,count/8,agents,dial)
        if (time.time() > (timeout + TIMEOUT_SECONDS)):
            print "timeout\n", timeout, time.time()
            #cleanup(count,cmdline)
            break

#calls = 204
calls = 95 #focus
print "dialing -", calls, "calls\n"
dials = ("55560", "3000", "3001", "70062", "4703","67892","4701","713300")
#dials = ("4703",)  # focus on a single Queue
#dials = ("8600",)  # Dev
agents = 5;
#agents = 1;
print dials
port = '5565'
#port = '5555'
args = shlex.split('/bin/netcat -u 127.0.0.1 ' + port)
try:
    p = Popen(args, stdin=PIPE, stdout=PIPE,stderr=PIPE, shell=False)
except:
    print 'could not connect to port', port
    sys.exit(-1)

nbsr = NBSR(p.stdout)
cmdline=p.stdin
timeout = time.time()
while (True):
    make_calls(cmdline,calls,agents,dials)

#    break  here for incomplete case. N.D.

    if (time.time() > (timeout + TIMEOUT_SECONDS)):
        print "timeout\n", timeout, time.time()
        cleanup(calls+2*agents,cmdline)
        break
    sleep(3)
    cleanup(calls+2*agents,cmdline)
    sleep(3)
    if (time.time() > (timeout + TIMEOUT_SECONDS)):
        print "timeout\n", timeout, time.time()
        break
p.kill()
