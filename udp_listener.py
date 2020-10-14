#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_DGRAM
maxsize = 4096
import random
import time
import select
sock = socket(AF_INET,SOCK_DGRAM)
sock.bind(('',3666))
sock.settimeout(2.0)
#sock.setblocking(0)
counter=0


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
                #sock.send('pong')
            else:
                time.sleep(0.1)
    except Exception as inst:
            print (type(inst))
            print (inst.args)
            print (inst)
            print (__file__, 'Oops')
            safe_exit()

while True:


    ready = select.select([sock], [], [], 0.5)
    if ready[0]:
        data, addr = sock.recvfrom(maxsize)
        counter += 1
        print ("addr = {}, data = {}, counter = {}".format(addr, data, counter));
        print ("counter = {}".format(counter));
   