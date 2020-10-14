#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_DGRAM
maxsize = 4096
import random
import time
import select

real_events=[
'Event: INVITE\nUniqNo: 65734\nDomain: siptalk64.xcastlabs.com\nDirection: CLN\nFrom: UC8xx-0001-01\nTo: 7160\n',
'Event: INVITE\nUniqNo: 65734\nDomain: siptalk64.xcastlabs.com\nDirection: CLN\nFrom: UC8xx-0001-01\nTo: 7160\n',
'Event: TALK\nUniqNo: 65734\nDomain: siptalk64.xcastlabs.com\nFMode: =\n',
'Event: BYE\nUniqNo: 65734\nDomain: siptalk64.xcastlabs.com\nDirection: SRV\n',
'Event: DTOR\nUniqNo: 65734\nDomain: siptalk64.xcastlabs.com\n',
'Event: REG\nDomain: siptalk64.xcastlabs.com\nLine: UC8xx-0001-01\nAOR: sip:UC8xx-0001-01*siptalk64.xcastlabs.com-75.145.154.225+5260@75.145.154.234:7064\nCallID: efd00b116ba451d@10.10.8.10\nAgent: Htek UC840 V1.0.4.2.11\nIntIP: 10.10.8.10\nExtIP: 75.145.154.225\n',
'Event: ACTIVE\nStarted: 1516742939\nRegs: 20\nDialogs: 0\nCalls: 0\nFull: 0\nExtra: R:20\n',
'Event: ACTIVE\nStarted: 1516742939\nRegs: 20\nDialogs: 0\nCalls: 0\nFull: 0\nExtra: R:20\n',
'Event: REG\nDomain: siptalk64.xcastlabs.com\nLine: UC8xx-0001-01\nAOR: sip:UC8xx-0001-01*siptalk64.xcastlabs.com-75.145.154.225+5260@75.145.154.234:7064\nCallID: efd00b116ba451d@10.10.8.10\nAgent: Htek UC840 V1.0.4.2.11\nIntIP: 10.10.8.10\nExtIP: 75.145.154.225\n',
'Event: ACTIVE\nStarted: 1516742939\nRegs: 20\nDialogs: 0\nCalls: 0\nFull: 0\nExtra: R:20\n',
'Event: ACTIVE\nStarted: 1516742939\nRegs: 20\nDialogs: 0\nCalls: 0\nFull: 0\nExtra: R:20\n',
'Event: FAILD\nDomain: siptalk64.xcastlabs.com\nLine: SPA303-0001-01\nCallID: 6a0fecd4-6f19d202@10.0.0.13\nAgent: Cisco/SPA303-7.6.2c\nIntIP: 10.0.0.13\nExtIP: 67.167.37.164\nReason: Not our Device\n',
'Event: REG\nDomain: siptalk64.xcastlabs.com\nLine: UC8xx-0001-01\nAOR: sip:UC8xx-0001-01*siptalk64.xcastlabs.com-75.145.154.225+5260@75.145.154.234:7064\nCallID: efd00b116ba451d@10.10.8.10\nAgent: Htek UC840 V1.0.4.2.11\nIntIP: 10.10.8.10\nExtIP: 75.145.154.225\n',
'Event: ACTIVE\nStarted: 1516742939\nRegs: 20\nDialogs: 0\nCalls: 0\nFull: 0\nExtra: R:20\n',
'Event: ACTIVE\nStarted: 1516742939\nRegs: 20\nDialogs: 0\nCalls: 0\nFull: 0\nExtra: R:20\n'
]
old_reg_event="""Event: REG
CallID: 1661796768_59574292@4.55.17.227
Domain: xcastlabs.voippbsite.net
Line: 7065D01L01
IntIP: 10.10.8.21
Hole: 75.145.154.225:2048
Agent: Cisco/SPA508G-7.6.2b
Timestamp: {}"""

old_unreg_event="""Event: UNREG
CallID: 1661796768_59574292@4.55.17.227
Domain: xcastlabs.voippbsite.net
Line: 7065D01L01
IntIP: 10.10.8.21
Hole: 75.145.154.225:2048
Agent: Cisco/SPA508G-7.6.2b
Timestamp: {}"""

reg_event="""Event: REG
Domain: siptalk64.xcastlabs.com
Line: 7065D06L01
AOR: sip:000a13ce4b919ae1-7065D06L01*siptalk64.xcastlabs.com-75.145.154.234+49388@75.145.154.234:7064
CallID: 8376a8a6-7383386a@10.10.8.74
Agent: Cisco/SPA508G-7.6.2b
IntIP: 10.10.8.74
ExtIP: 75.145.154.225"""

unreg_event="""Event: UNREG
Domain: siptalk64.xcastlabs.com
Line: 1113D01L01
AOR: sip:1113D01L01*siptalk64.xcastlabs.com-75.145.154.225+9901@75.145.154.234:7064"""


def generate_event():
    event_index=random.randint(0,len(real_events)-1)
    return real_events[event_index]

sock = socket(AF_INET,SOCK_DGRAM)
sock.bind(('',12345))
sock.settimeout(2.0)
#sock.setblocking(0)
counter=0

sender_sock = socket(AF_INET,SOCK_DGRAM)

while True:
    ready = select.select([sock], [], [], 0.5)
    if ready[0]:
        data, addr = sock.recvfrom(maxsize)
        counter += 1
        #print ("addr = {}, data = {}, counter = {}".format(addr, data, counter));
        print ("counter = {}".format(counter));
        if('127.0.0.1' == addr[0]):
            resp = generate_event()
            #b'UDP server sending data'
            sender_sock.sendto(resp.encode('utf-8'),('bdsupportdb-02.siptalk.com', 54321))
    
 