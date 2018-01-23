#!/usr/bin/env python
from socket import socket, AF_INET, SOCK_DGRAM
MAX_SIZE=4096
import time

def to_db(line):
    parts=line.strip().split("\\n")
    if(len(parts)< 1): return None
    fields={}
    for f in parts:
        if(0 < f.find(":")):
            #print("to_db: f = " +f)
            key, value = f.strip().split(": ")
            fields[key.strip()] = value.strip()
    fields["Event"]=fields["'Event"].strip()
    del fields["'Event"]
    fields["time"] = int(time.time() * 1000000000)
    return fields

if __name__ == '__main__':
    sock = socket(AF_INET,SOCK_DGRAM)
    sock.bind(('',54321))
    msg = "Hello UDP server"
    while True:
        #time.sleep(300)
        data, addr = sock.recvfrom(MAX_SIZE)
        record=to_db(repr(data))
        ev_type=record["Event"]
        print ("ev_type: ", ev_type)
        print(record)
        #print (record)
        #print("Server says:{}".format(repr(process_event(data))))
