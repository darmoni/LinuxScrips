#!/usr/bin/env python

import socket, time, sys
from threading import Thread
import signal


def sig_handler(sig, frame):
    print "got sig(%d) \n" % sig
    safe_exit()

signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)

resources=[]

def safe_exit():
    for r in resources:
        del r
    exit(0)

PORT = 32802
BUFFER_SIZE = 4096

def read_from_middle(s):
    try:
        while s:
            data, addr = s.recvfrom(BUFFER_SIZE)
            if(data):
                when=time.time()
                data += "Time: {:18.9f}\nServerIP: {}\n".format(when,addr[0])
                #print(data)
                print(repr(data.strip()).strip("'"))
            else:
                time.sleep(1)
    except:
        sys.exit(-1)
    if(s):
        s.close()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', PORT))
middle_worker = Thread(target=read_from_middle, args=(s,))
middle_worker.setDaemon(True)
middle_worker.start()
resources.append(middle_worker)
while middle_worker:
    time.sleep(3)
middle_worker.join()
