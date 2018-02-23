#!/usr/bin/env python

from sys import stdin
import time

def to_db(line):
    print("to_db: " + line)
    if(line.find("\\n") > 0):
        parts=line.strip().split("\\n")
    elif(line.find("\n") > 0):
        parts=line.strip().split("\n")
    if(parts and len(parts)< 1): return None
    fields={}
    for f in parts:
        if(0 < f.find(":")):
            #print("to_db: f = " +f)
            key, value = f.strip().split(": ")
            fields[key.strip()] = value.strip()
    fields["time"] = int(time.time() * 1000000000)
    return fields

if __name__ == '__main__':
    while True:
        data = stdin.readline()
        record=to_db(data)
        if(record):
            print(record)#print(repr(data))
