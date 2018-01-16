#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_DGRAM
maxsize = 4096
import random
import time
import select

reg_event="""Event: REG
CallID: 1661796768_59574292@4.55.17.227
Domain: xcastlabs.voippbsite.net
Line: 7065D01L01
IntIP: 10.10.8.21
Hole: 75.145.154.225:2048
Agent: Cisco/SPA508G-7.6.2b
Timestamp: {}"""

unreg_event="""Event: UNREG
CallID: 1661796768_59574292@4.55.17.227
Domain: xcastlabs.voippbsite.net
Line: 7065D01L01
IntIP: 10.10.8.21
Hole: 75.145.154.225:2048
Agent: Cisco/SPA508G-7.6.2b
Timestamp: {}"""

def generate_event():
    if(4 > random.randint(1, 6)):
        return unreg_event.format(int(time.time()))
    else:
        return reg_event.format(int(time.time()))

sock = socket(AF_INET,SOCK_DGRAM)
sock.bind(('',12345))
sock.settimeout(2.0)
#sock.setblocking(0)
counter=0

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
            sock.sendto(resp.encode('utf-8'),addr)
    
