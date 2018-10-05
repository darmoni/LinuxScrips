#!/usr/bin/env python3

import signal, time
from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import os.path

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

def pinger(port):

    while True:
        try:
            PORT = port
            sock = socket(AF_INET,SOCK_DGRAM)
            server_alive=True
            while server_alive:
                for site in ("www.google.com", "darmoni.us", "yahoo.com"):
                    msg = "{}\n".format(site).encode('utf-8')
                    #print(msg)
                    sock.sendto(msg, ('', PORT))
                    #sock.flush()
                server_alive=False
                data=None
                data, addr = sock.recvfrom(MAX_SIZE)
                if data:
                    print("Received '{}'".format(data))
                    server_alive=True
                if not server_alive:
                    return
                time.sleep(0.5)

        except Exception as inst:
                print (type(inst))
                print (inst.args)
                print (inst)
                print (__file__, 'Oops')
                safe_exit()

if __name__ == '__main__':
    pinger(32803)












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

