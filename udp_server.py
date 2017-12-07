#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_DGRAM
maxsize = 4096

sock = socket(AF_INET,SOCK_DGRAM)
sock.bind(('',12345))
counter=0
while True:
    
    data, addr = sock.recvfrom(maxsize)
    counter += 1
    #print ("addr = {}, data = {}, counter = {}".format(addr, data, counter));
    print ("counter = {}".format(counter));
    if('127.0.0.1' == addr[0]):
        resp = b'UDP server sending data'
        sock.sendto(resp,addr)
    
