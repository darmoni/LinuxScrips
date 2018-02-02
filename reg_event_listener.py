#!/usr/bin/env python

"""
DROP TABLE IF EXISTS invite_table;
CREATE TABLE  invite_table
(
recdate Date MATERIALIZED toDate(time)
, direction String, domain String, event String, from String, serverip String, time Float64, to String, uniqno String
)
ENGINE = MergeTree(recdate, (recdate,serverip), 8192);
#PARTITION BY recdate ORDER BY recdate;

insert into invite_table (domain,from,direction,serverip,uniqno,to,time,event) values('siptalk64.xcastlabs.com','GS0001-0001-02','CLN','10.10.10.62','84330','9801',1517236893.594013929,'INVITE');
insert into invite_table (domain,from,direction,serverip,uniqno,to,time,event) values('siptalk64.xcastlabs.com','GS0001-0001-02','CLN','10.10.10.62','84330','9801',1517236893.633804083,'INVITE');
DROP TABLE IF EXISTS talk_table;
CREATE TABLE  talk_table
(
recdate Date MATERIALIZED toDate(time)
, domain String, event String, fmode String, serverip String, time Float64, uniqno String
)
ENGINE = MergeTree(recdate, (recdate,serverip), 8192);
#PARTITION BY recdate ORDER BY recdate;

insert into talk_table (domain,serverip,uniqno,fmode,time,event) values('siptalk64.xcastlabs.com','10.10.10.62','84330','-',1517236894.690232038,'TALK');
DROP TABLE IF EXISTS bye_table;
CREATE TABLE  bye_table
(
recdate Date MATERIALIZED toDate(time)
, direction String, domain String, event String, serverip String, time Float64, uniqno String
)
ENGINE = MergeTree(recdate, (recdate,serverip), 8192);
#PARTITION BY recdate ORDER BY recdate;

insert into bye_table (domain,direction,serverip,uniqno,time,event) values('siptalk64.xcastlabs.com','SRV','10.10.10.62','84330',1517236894.897785902,'BYE');
DROP TABLE IF EXISTS reg_table;
CREATE TABLE  reg_table
(
recdate Date MATERIALIZED toDate(time)
, aor String, agent String, callid String, domain String, event String, extip String, intip String, line String, serverip String, time Float64
)
ENGINE = MergeTree(recdate, (recdate,serverip), 8192);
#PARTITION BY recdate ORDER BY recdate;

insert into reg_table (domain,callid,intip,agent,serverip,aor,time,line,extip,event) values('siptalk64.xcastlabs.com','efd00b116ba451d@10.10.8.10','10.10.8.10','Htek UC840 V1.0.4.2.11','10.10.10.62','sip:UC8xx-0001-01*siptalk64.xcastlabs.com-75.145.154.225+5260@75.145.154.234:7064',1517236907.523650885,'UC8xx-0001-01','75.145.154.225','REG');
insert into reg_table (domain,callid,intip,agent,serverip,aor,time,line,extip,event) values('siptalk64.xcastlabs.com','7446951c3234ab298082901156869702','10.10.8.210','Polycom/5.5.0.20556 PolycomVVX-VVX_410-UA/5.5.0.20556','10.10.10.62','sip:POL500-0003-01*siptalk64.xcastlabs.com-75.145.154.225+41742@75.145.154.234:7064',1517236925.390005112,'POL500-0003-01','75.145.154.225','REG');
DROP TABLE IF EXISTS dtor_table;
CREATE TABLE  dtor_table
(
recdate Date MATERIALIZED toDate(time)
, domain String, event String, serverip String, time Float64, uniqno String
)
ENGINE = MergeTree(recdate, (recdate,serverip), 8192);
#PARTITION BY recdate ORDER BY recdate;

insert into dtor_table (uniqno,domain,event,serverip,time) values('84330','siptalk64.xcastlabs.com','DTOR','10.10.10.62',1517236934.897223949);
DROP TABLE IF EXISTS faild_table;
CREATE TABLE  faild_table
(
recdate Date MATERIALIZED toDate(time)
, agent String, callid String, domain String, event String, extip String, intip String, line String, reason String, serverip String, time Float64
)
ENGINE = MergeTree(recdate, (recdate,serverip), 8192);
#PARTITION BY recdate ORDER BY recdate;

insert into faild_table (domain,callid,intip,agent,reason,serverip,time,line,extip,event) values('siptalk64.xcastlabs.com','4c2ad322-23efe7fa@10.0.0.13','10.0.0.13','Cisco/SPA303-7.6.2c','Not our Device','10.10.10.62',1517236985.137672901,'SPA303-0001-01','67.167.37.164','FAILD');

DROP TABLE IF EXISTS active_table;
CREATE TABLE  active_table
(
recdate Date MATERIALIZED toDate(time)
, calls String, dialogs String, event String, extra String, full String, regs String, serverip String, started String, time Float64
)
ENGINE = MergeTree(recdate, (recdate,serverip), 8192);
#PARTITION BY recdate ORDER BY recdate;

DROP TABLE IF EXISTS srv_audio_table;
CREATE TABLE  srv_audio_table
(
recdate Date MATERIALIZED toDate(time)
, domain String, event String, from String, serverip String, time Float64, uniqno String
)
ENGINE = MergeTree(recdate, (recdate,serverip), 8192);
#PARTITION BY recdate ORDER BY recdate;

insert into srv_audio_table (domain,from,serverip,uniqno,time,event) values('russ.xcastlabs.com','75.145.154.234:43720','10.10.10.62','84593',1517244033.519648075,'SRV_AUDIO');
DROP TABLE IF EXISTS cln_audio_table;
CREATE TABLE  cln_audio_table
(
recdate Date MATERIALIZED toDate(time)
, domain String, event String, from String, serverip String, time Float64, uniqno String
)
ENGINE = MergeTree(recdate, (recdate,serverip), 8192);
#PARTITION BY recdate ORDER BY recdate;

DROP TABLE IF EXISTS cln_video_table;
CREATE TABLE  cln_video_table
(
recdate Date MATERIALIZED toDate(time)
, domain String, event String, from String, serverip String, time Float64, uniqno String
)
ENGINE = MergeTree(recdate, (recdate,serverip), 8192);
#PARTITION BY recdate ORDER BY recdate;


insert into active_table (full,dialogs,calls,extra,started,regs,serverip,time,event) values('0','0','0','R:22','1516742939','22','10.10.10.62',1517237039.363743067,'ACTIVE');
insert into reg_table (domain,callid,intip,agent,serverip,aor,time,line,extip,event) values('russ.xcastlabs.com','5326ef0a-c226ff31@10.0.0.207','10.0.0.207','Linksys/SPA1001-3.1.19(SE)','10.10.10.62','sip:312D01L01*russ.xcastlabs.com-67.167.37.164+16195@75.145.154.234:7064',1517237115.241877079,'312D01L01','67.167.37.164','REG');
insert into reg_table (domain,callid,intip,agent,serverip,aor,time,line,extip,event) values('siptalk64.xcastlabs.com','1471544780@192.168.1.173','192.168.1.173','Yealink SIP-T22P 7.73.193.50','10.10.10.62','sip:7131YL01*siptalk64.xcastlabs.com-173.15.117.197+35932@75.145.154.234:7064',1517237244.529793024,'7131YL01','173.15.117.197','REG');
insert into invite_table (domain,from,direction,serverip,uniqno,to,time,event) values('siptalk64.xcastlabs.com','GS0001-0001-02','CLN','10.10.10.62','84345','9801',1517237287.197594881,'INVITE');
insert into invite_table (domain,from,direction,serverip,uniqno,to,time,event) values('siptalk64.xcastlabs.com','GS0001-0001-02','CLN','10.10.10.62','84345','9801',1517237287.235697985,'INVITE');
insert into talk_table (domain,serverip,uniqno,fmode,time,event) values('siptalk64.xcastlabs.com','10.10.10.62','84345','-',1517237287.302793980,'TALK');
insert into bye_table (domain,direction,serverip,uniqno,time,event) values('siptalk64.xcastlabs.com','SRV','10.10.10.62','84345',1517237321.107734919,'BYE');
insert into active_table (full,dialogs,calls,extra,started,regs,serverip,time,event) values('0','2','0','R:22,-:1','1516742939','22','10.10.10.62',1517237339.364963055,'ACTIVE');
insert into dtor_table (uniqno,domain,event,serverip,time) values('84345','siptalk64.xcastlabs.com','DTOR','10.10.10.62',1517237361.107492924);
insert into srv_audio_table (domain,from,serverip,uniqno,time,event) values('russ.xcastlabs.com','75.145.154.234:43720','10.10.10.62','84593',1517244033.519648075,'SRV_AUDIO');
insert into cln_audio_table (domain,from,serverip,uniqno,time,event) values('russ.xcastlabs.com','75.145.154.225:58276','10.10.10.62','84593',1517244033.573282957,'CLN_AUDIO');
insert into cln_video_table (domain,from,serverip,uniqno,time,event) values('russ.xcastlabs.com','75.145.154.225:46124','10.10.10.62','84593',1517244033.586697102,'CLN_VIDEO');

"""

from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname
MAX_SIZE=4096
import time, sys, re
from Queue import Queue
from threading import Thread

from clickhouse_driver import Client
import ConfigParser as configparser
import log
from connection import Connection
import signal

resources=[]
def safe_exit():
    for r in resources:
        del r
    exit(0)

def sig_handler(sig, frame):
    print ("got sig(%d)\n" % sig)
    safe_exit()

signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)

#print(client.execute('SHOW TABLES;'))

xcast_event_tables={}
non_string_fields={'Time':'Float64'}
fields_with_ports=['from',]


def separate_addr_port(key, value,fields):
    if(key.lower() in fields_with_ports):
        m=re.match(r"(.+):(\d+)$",value)
        if m:
            fields[key.strip()]=m.group(1).strip()
            fields[key.strip()+'_port']=m.group(2).strip()
            return True
    return False

def translate_field(x,v):
    return {
        'int': int(float(v)),
        'float64': float(v),
    }.get(x.lower(), v)

class xcast_event_table:

    def print_table(self):
        if self.table_name in xcast_event_tables:
            return(self.create_new_table)

    def __init__(self,record,ev_type,table_name,even_if_exists=False):
        self.table_name = table_name
        if( table_name in xcast_event_tables):
            self.create_new_table=''
            pass
        else:
            drop_old_table="DROP TABLE IF EXISTS {};".format(table_name)
            other_fields=''
            create_even_if_exists= ("IF NOT EXISTS ",drop_old_table) [even_if_exists]
            for key in sorted(record.keys()):
                if (key in non_string_fields): 
                    type_name=non_string_fields[key]
                else:
                    type_name='String'
                other_fields += (", {} {}".format(key.lower(), type_name))
            self.create_new_table="""CREATE TABLE {} {}
(
recdate Date MATERIALIZED toDate(time)
{}
)
ENGINE = MergeTree(recdate, (recdate,serverip), 8192);
""".format(create_even_if_exists, table_name, other_fields)
            xcast_event_tables.update({self.table_name:self.create_new_table})
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
            if not separate_addr_port(key, value,fields):
                fields[key.strip()] = value.strip()
    #print(fields)
    q.put(fields)

def prepare_insert_query(q,client):
    try:
        if not client:
            safe_exit()
        ping="show tables;\n".encode('utf-8')
        #print(client.execute(ping)) # testing
        while client:
            record=q.get()
            if(record):
                #create_table.print_tables()
                ev_type=record["Event"]
                table_name='middle_events_'+ev_type.lower()
                
                field_names=(",".join(record.keys())).lower()
                record_values=[]
                for k in record.keys():
                    if (k in non_string_fields):
                        value = translate_field(non_string_fields[k],record[k])
                    else:
                        value = str(record[k])
                    record_values.append(value)
                record_values=tuple(record_values)
                #field_values=",".join(record_values)
                query="""INSERT INTO {} ({}) VALUES""".format(table_name,field_names).encode('utf-8')
                #query += "{}='{}'".format("Event".lower(),record["Event"])
                #del record["Event"]
                #query += ", {}={}".format("Time".lower(),record["Time"])
                #del record["Time"]
                #for key in sorted(record.keys()):
                #    value = record[key]
                #    query += (", {}='{}'".format(key.lower(),value))
                try:
                    if(query and len(record_values)>0):
                        print(query,[record_values])
                        event_processor=xcast_event_table(record,ev_type,table_name)
                        if event_processor:
                            create_table=event_processor.print_table().encode('utf-8')
                            if(create_table):
                                print(client.execute(create_table))
                        print(client.execute(query,[record_values],types_check=True))
                except Exception as inst:
                    print type(inst)
                    print inst.args
                    print inst
                    print __file__, 'Oops'
            #del record
            q.task_done()
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        print __file__, 'Oops'
    safe_exit()

def read_from_middle(sock,events_q):
    while True:
        data, addr = sock.recvfrom(MAX_SIZE)
        #print(msg)
        if(data):
            when=time.time()
            data += "\nTime: {:18.9f} \nServerIP: {}".format(when, addr[0])
            to_db(data,events_q)
        else:
            time.sleep(1)

def collect_middle_events(client):
    sock = socket(AF_INET,SOCK_DGRAM)
    sock.bind(('',32802))
    msg = "Hello UDP server"
    events_q = Queue(maxsize=0)
    #db_cmd_q = Queue(maxsize=0)
    worker = Thread(target=prepare_insert_query, args=(events_q,client))
    worker.setDaemon(True)
    worker.start()
    for i in range(1):
        middle_worker = Thread(target=read_from_middle, args=(sock,events_q))
        middle_worker.setDaemon(True)
        middle_worker.start()

    while True:
        if client:
            time.sleep(2)
        else:
            safe_exit()
        #db_cmd=db_cmd_q.get()
        #if(db_cmd):
        #    print((repr(db_cmd)))
        #    db_cmd_q.task_done()

if __name__ == '__main__':
    file_config = configparser.ConfigParser()
    file_config.read(['setup.cfg'])
    log.configure(file_config.get('log', 'level'))
    
    host = file_config.get('db', 'host')
    #port = file_config.getint('db', 'port') using default port
    database = file_config.get('db', 'database')
    user = file_config.get('db', 'user')
    password = file_config.get('db', 'password')
    compression=file_config.get('db', 'compression') 
    #print (host, port, database, user, password)
    client = Client(host=host, database=database, user=user, password=password,compression=compression)
    resources.append(client)
    try:
        collect_middle_events(client)
        safe_exit()
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        print __file__, 'Oops'
    safe_exit()
