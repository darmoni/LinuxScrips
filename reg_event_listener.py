#!/usr/bin/env python

"""
insert into active_table event='ACTIVE', time=1516925339374555136, calls='0', dialogs='0', extra='R:21', full='0', regs='21', serverip='10.10.10.62', started='1516742939'
insert into bye_table event='BYE', time=1516925264825032960, direction='CLN', domain='siptalk64.xcastlabs.com', serverip='10.10.10.62', uniqno='72806'
insert into cancel_table event='CANCEL', time=1516976718519753984, direction='SRV', domain='siptalk64.xcastlabs.com', serverip='10.10.10.62', uniqno='74545'
insert into dtor_table event='DTOR', time=1516925304825748992, domain='siptalk64.xcastlabs.com', serverip='10.10.10.62', uniqno='72806'
insert into faild_table event='FAILD', time=1516925728514002944, agent='Cisco/SPA303-7.6.2c', callid='6a0fecd4-6f19d202@10.0.0.13', domain='siptalk64.xcastlabs.com', extip='67.167.37.164', intip='10.0.0.13', line='SPA303-0001-01', reason='Not our Device', serverip='10.10.10.62'
insert into invite_table event='INVITE', time=1516925232999401216, direction='CLN', domain='siptalk64.xcastlabs.com', from='GS0001-0001-02', serverip='10.10.10.62', to='9801', uniqno='72806'
insert into reg_table event='REG', time=1516925236676583168, aor='sip:TestVVXPOL401L02*siptalk64.xcastlabs.com-75.145.154.225+16053@75.145.154.234:7064', agent='PolycomVVX-VVX_401-UA/5.7.0.11768', callid='03ba66a09b5f474da3abd51c91016a63', domain='siptalk64.xcastlabs.com', extip='75.145.154.225', intip='10.10.8.46', line='TestVVXPOL401L02', serverip='10.10.10.62'
insert into talk_table event='TALK', time=1516925233086228992, domain='siptalk64.xcastlabs.com', fmode='-', serverip='10.10.10.62', uniqno='72806'
insert into unreg_table event='UNREG', time=1516925303046435072, aor='sip:GS0001-0001-02-0x1706800*siptalk64.xcastlabs.com-75.145.154.225+45338@75.145.154.234:7064', domain='siptalk64.xcastlabs.com', line='GS0001-0001-02-0x1706800', serverip='10.10.10.62'
"""
from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname
MAX_SIZE=4096
import time
from Queue import Queue
from threading import Thread

xcast_event_tables={}
non_string_fields={'Time':'UInt64', 'Unix_TS':'UInt64'}

class xcast_event_table:

    def print_tables(self):
        print(xcast_event_tables)

    def __init__(self,record,ev_type,table_name):
        if( table_name in xcast_event_tables):
            pass
        else:
            other_fields=''
            for key in sorted(record.keys()):
                if (key in non_string_fields): 
                    type_name=non_string_fields[key]
                else:
                    type_name='String'
                other_fields += (", {} {}".format(key.lower(), type_name))
            create_new_table="""CREATE TABLE {}
(
recdate Date MATERIALIZED toDate(unix_ts)
{}
)
ENGINE = MergeTree(recdate, (recdate,serverip), 8192);
#PARTITION BY recdate ORDER BY recdate;
""".format(table_name, other_fields)
            print(create_new_table)
            xcast_event_tables.update({table_name:create_new_table})
    def __del__ (self):
        pass


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
            #create_table.print_tables()
            ev_type=record["Event"]
            table_name=ev_type.lower()+'_table'
            create_table=xcast_event_table(record,ev_type,table_name)
            
            field_names=(",".join(record.keys())).lower()
            record_values=[]
            for k in record.keys():
                if (k in non_string_fields):
                    value = record[k]
                else:
                    value = "'"+record[k]+"'"
                record_values.append(value)
            field_values=",".join(record_values)
            query="insert into {} ({}) values({});".format(table_name,field_names,field_values)
            #query += "{}='{}'".format("Event".lower(),record["Event"])
            #del record["Event"]
            #query += ", {}={}".format("Time".lower(),record["Time"])
            #del record["Time"]
            #for key in sorted(record.keys()):
            #    value = record[key]
            #    query += (", {}='{}'".format(key.lower(),value))
            #print(query)
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
            when=time.time()
            data += "\nUnix_TS: {} \nTime: {} \nServerIP: {}".format(int(when),int(when * 1000000000), addr[0])
            to_db(data,events_q)

