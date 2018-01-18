#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_DGRAM
maxsize = 4096
import random
import time
import select

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
    if(500 > random.randint(0, 1000)):
        return unreg_event#.format(int(time.time()))
    else:
        return reg_event#.format(int(time.time()))

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
            sender_sock.sendto(resp.encode('utf-8'),('', 54321))
    
