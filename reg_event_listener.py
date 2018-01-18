#!/usr/bin/env python
from socket import socket, AF_INET, SOCK_DGRAM
MAX_SIZE=4096
import time

if __name__ == '__main__':
    sock = socket(AF_INET,SOCK_DGRAM)
    sock.bind(('',54321))
    msg = "Hello UDP server"
    while True:
        #time.sleep(300)
        data, addr = sock.recvfrom(MAX_SIZE)
        print(repr(data))
        #print("Server says:{}".format(repr(process_event(data))))
