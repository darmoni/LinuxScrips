#!/usr/bin/env python

import argparse, sys
import shlex
from subprocess import call, Popen, check_call, check_output, PIPE, CalledProcessError
from weakref import WeakValueDictionary
import os
import signal

def sig_handler(sig, frame):
    print "got sig({})\n".format(sig)
    safe_exit(sig)

signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)

def safe_exit(level):
    # save stuff
    print("Exiting ...\n")
    exit(0)

try:
    lines = "wc -l logs/pbx-node2-hstarter.log\n"
    pairs = "grep 'tachPair' logs/pbx-node2-hstarter.log | wc -l\n"
    ssh_cmd='ssh xcast@logserver3-la.siptalk.com '
    args = shlex.split(ssh_cmd + lines)
    total_lines = int(shlex.split(check_output(args))[0])
    args = shlex.split(ssh_cmd + pairs)
    total_pairs = int(shlex.split(check_output(args))[0])
    print ("loading is {:05.2f}%".format(100.0*total_pairs/total_lines))

except Exception as inst:
    print (type(inst))
    print (inst.args)
    print (inst)
    print (__file__, 'Oops')
