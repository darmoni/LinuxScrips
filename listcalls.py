#!/usr/bin/env python

from time import sleep
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read
import shlex, subprocess
import socket
import os
from subprocess import call, Popen, check_output, PIPE

args = shlex.split('/bin/netcat -u 127.0.0.1 5565')
p1 = Popen(args, stdin=PIPE, stdout=PIPE,stderr=PIPE, shell=False)

# set the O_NONBLOCK flag of p.stdout file descriptor:
flags = fcntl(p1.stdout, F_GETFL) # get current p.stdout flags
fcntl(p1.stdout, F_SETFL, flags | O_NONBLOCK)

p1.stdin.write("l")
sleep(0.1)

while True:
    try:
        print read(p1.stdout.fileno(), 1024)
    except OSError:
        # the os throws an exception if there is no data
        print '[no more data]'
        break


#p2 = Popen(["grep","List of active calls"], stdin=p1.stdout, stdout=PIPE)
#(stdoutdata, stderrdata) = p1.communicate(input="l\n")
#print stdoutdata

