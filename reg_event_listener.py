#!/usr/bin/env python

"""
insert into invite_table event='INVITE', time=1516925084911087104, direction='CLN', domain='siptalk64.xcastlabs.com', from='GS0001-0001-02', serverip='10.10.10.62', to='9801', uniqno='72801'
insert into talk_table event='TALK', time=1516925084999950848, domain='siptalk64.xcastlabs.com', fmode='-', serverip='10.10.10.62', uniqno='72801'
insert into bye_table event='BYE', time=1516925107237929984, direction='CLN', domain='siptalk64.xcastlabs.com', serverip='10.10.10.62', uniqno='72802'
insert into reg_table event='REG', time=1516925134176752128, aor='sip:TestVVXPOL410L01*russ.xcastlabs.com-75.145.154.225+16053@75.145.154.234:7064', agent='PolycomVVX-VVX_401-UA/5.7.0.11768', callid='c5dc76e65ae746cbcbe5f96dbf016a63', domain='russ.xcastlabs.com', extip='75.145.154.225', intip='10.10.8.46', line='TestVVXPOL410L01', serverip='10.10.10.62'
insert into dtor_table event='DTOR', time=1516925147238095104, domain='siptalk64.xcastlabs.com', serverip='10.10.10.62', uniqno='72802'
insert into dtor_table event='DTOR', time=1516925147890331904, domain='siptalk64.xcastlabs.com', serverip='10.10.10.62', uniqno='72801'
"""
from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname
MAX_SIZE=4096
import time
from Queue import Queue
from threading import Thread

def to_db(line,q):
    parts=line.replace("\\n","\n").split("\n")
    if(len(parts)< 1):
        return None
    if('Event' != parts[0].strip().split(": ")[0]):
        return None

    fields={}
    for f in parts:
        if(0 < f.find(":")):
            key, value = f.strip().split(": ")
            fields[key.strip()] = value.strip()
    q.put(fields)

def prepare_insert_query(q):
    while True:
        record=q.get()
        if(record):
            ev_type=record["Event"]
            table_name=ev_type.lower()+'_table'
            query="insert into {} ".format(table_name)
            query += "{}='{}'".format("Event".lower(),record["Event"])
            del record["Event"]
            query += ", {}={}".format("Time".lower(),record["Time"])
            del record["Time"]
            for key in sorted(record.keys()):
                value = record[key]
                query += (", {}='{}'".format(key.lower(),value))
            print(query)
        q.task_done()

if __name__ == '__main__':
    sock = socket(AF_INET,SOCK_DGRAM)
    sock.bind(('',32802))
    msg = "Hello UDP server"
    events_q = Queue(maxsize=0)
    for i in range(5):
      worker = Thread(target=prepare_insert_query, args=(events_q,))
      worker.setDaemon(True)
      worker.start()
    while True:
        data, addr = sock.recvfrom(MAX_SIZE)
        #print(msg)
        if(data):
            data += "\nTime: {} \nServerIP: {}".format(int(time.time() * 1000000000), addr[0])
            to_db(data,events_q)

