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
        call = "|"+who+"\n"
#        print call
        cmdline.write(call)
        sleep (3)
        cmdline.write("T") # audio loop back

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

TIMEOUT_SECONDS = 14*60

def testing(count, agents, dial):
    global cmdline

    timeout = time.time()
    make_calls(cmdline,count,agents,dial)
    timeoutStarted = True

#calls = 204
calls = 1 #focus
print "dialing -", calls, "calls\n"
dials = ("PRD Make call and send audio")

agents = 1;
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
cmdline.write("/auloop\n")

while (True):
    make_calls(cmdline,calls,agents,dials)

#    break  here for incomplete case. N.D.

    if (time.time() > (timeout + TIMEOUT_SECONDS)):
        print "timeout\n", timeout, time.time()
        cleanup(calls+2*agents,cmdline)
        break
    sleep(300)
    cleanup(calls+2*agents,cmdline)
    sleep(30)
    if (time.time() > (timeout + TIMEOUT_SECONDS)):
        print "timeout\n", timeout, time.time()
        break
p.kill()
