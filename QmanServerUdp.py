#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_DGRAM
maxsize = 4096
import random
import time
import select

from QmanServer import handle_event

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
            resp = handle_event(data)
            sender_sock.sendto(resp.encode('utf-8'),addr)

