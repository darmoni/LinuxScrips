#!/usr/bin/env python

#ident $Id$ $Date$

import shlex, subprocess
import socket
import os
import time
from time import sleep
from subprocess import call, Popen, check_output, PIPE
from nbstreamreader import NonBlockingStreamReader as NBSR
import signal
import sys, getopt

global workers

def safe_exit(level):
    global workers
    print 'Killing Server', "len(workers) = {}".format(len(workers))
    for test_server in wait(workers):
        if (test_server):
            test_server.stdin.write("q\n")
            sleep(0.1)
            test_server.terminate()
            workers.remove(test_server)
    exit(0)

def sig_handler(sig, frame):
    print "got sig(", sig,")\n"
    safe_exit(sig)

signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)

def start_baresip(user, server):
    HOST="ssh "+user+"@"+server
    # Ports are handled in ~/.ssh/config since we use OpenSSH
    COMMAND="nohup baresip < /dev/null"

    args = shlex.split(HOST+" "+ COMMAND)
    ssh = Popen(args,stdin=PIPE,stdout=PIPE,stderr=PIPE, shell=False)
    return ssh

TIMEOUT_SECONDS = 24*60*60 # 24 hours are enough ?
def main(argv):
    global workers
    workers = []
    testserver = 'bairsip.xcastlabs.com'
    timeout = time.time()
    try:
      opts, args = getopt.getopt(argv,"ht:l:",["testserver=","logserver="])
    except getopt.GetoptError:
      print __FILE__, ' -t <testserver>'
      exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print __file__, ' -t <testserver>'
         exit()
      elif opt in ("-t", "--testserver"):
         testserver = arg

    print  "Starting",   (time.strftime("%H:%M:%S"))
    try:
        test_server = start_baresip("nir",testserver);
        if (test_server):
            workers.append(test_server)
        else:
            exit(-1)
        events= NBSR(test_server.stdout)
        print 'Testing from', testserver, 'has started, and will kill itself in 24 hours'
        while(True):
            sleep(60)
            while True: #empty the trash
              try:
                line =results.readline()
                if(None == line):
                    break
              except:
                break

            if (time.time() > (timeout + TIMEOUT_SECONDS)):
                print "timeout\n", timeout, time.time()
                break
        print  "Time is over", "Killing the server",   (time.strftime("%H:%M:%S"))
        test_server.stdin.write("q\n")
        sleep(0.1)
        test_server.terminate()
    except:
        exit(0)

if __name__ == "__main__":
   main(sys.argv[1:])
