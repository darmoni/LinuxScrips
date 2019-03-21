#!/usr/bin/env python3

import signal, time
from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import os.path
import resource

MAX_SIZE=4096



resources=[]
def safe_exit():
    counter=1
    for r in resources:
        print ("deleting {}\n".format(counter))
        del r
        counter +=1
    exit(0)

def sig_handler(sig, frame):
    print ("got sig(%d)\n" % sig)
    safe_exit()

signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)

dummy_invite_collector_record='''Event: INVITE
UniqNo: 134313
Domain: not_listed.neverland.oops
Direction: CLN
From: SPA942-0001-02
To: 09
Self: 0.0.0.0:0607
'''

dummy_active_collector_record='''Event: ACTIVE
Started: 1550679070
Regs: 26
Dialogs: 0
Calls: 0
Full: 0
Extra: R:26
Self: 0.0.0.0:0607
'''

dummy_reg_collector_record='''Event: REG
Domain: not_listed.neverland.oops
Line: UC8xx-0001-01
AOR: sip:UC8xx-0001-01*siptalk64.xcastlabs.com-75.145.154.225+5260@75.145.154.234:7064
CallID: e483198c48b0a5e@10.10.8.6
Agent: Htek UC840 V1.0.4.2.11
IntIP: 10.10.8.6:5260
ExtIP: 75.145.154.225:5260
Self: 0.0.0.0:0607
'''
#msg = "ping"
msg = dummy_invite_collector_record
#msg = dummy_reg_collector_record
#msg = dummy_active_collector_record
def pinger(port):
    try:

        PORT = port
        sock = socket(AF_INET,SOCK_DGRAM)
        for counter in range(0,300000):
            #print(msg)
            sock.sendto(msg.encode('utf-8'),('', PORT))
            #data, addr = sock.recvfrom(MAX_SIZE)
            #print("Received '{}' back after sending '{}'".format(data.decode(),msg))
            time.sleep(0.001)
            if counter % 5000 == 0:
                #pass
                time.sleep(1)
            if counter % 5000 == 0:
                #pass
                print(counter)
        return

    except Exception as inst:
            print (type(inst))
            print (inst.args)
            print (inst)
            print (__file__, 'Oops')
            safe_exit()
    safe_exit()

if __name__ == '__main__':
    pinger(32802)

def ponger(port):
    try:
        sock = socket(AF_INET,SOCK_DGRAM)
        sock.bind(('',port))
        print ("port={}".format(port))
        while True:
            data, addr = sock.recvfrom(MAX_SIZE)
            print(data, addr)
            if(data):
                print(data)
                sock.send('pong')
            else:
                time.sleep(0.1)
    except Exception as inst:
            print (type(inst))
            print (inst.args)
            print (inst)
            print (__file__, 'Oops')
            safe_exit()

