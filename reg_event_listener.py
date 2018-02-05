#!/usr/bin/env python

"""
CREATE TABLE monitoring.middle_active ( calls String,  dialogs String,  event String,  extra String,  full String,  regs String,  serverip String,  started String,  time Float64,  recdate Date MATERIALIZED toDate(time)) ENGINE = MergeTree(recdate, (recdate, serverip), 8192)
CREATE TABLE monitoring.middle_registration ( agent String,  aor String,  callid String,  domain String,  event String,  extip String,  intip String,  line String,  reason String,  serverip String,  time Float64,  recdate Date MATERIALIZED toDate(time)) ENGINE = MergeTree(recdate, (recdate, serverip), 8192)
CREATE TABLE monitoring.middle_call ( direction String,  domain String,  event String,  extra String,  fmode String,  from String,  from_port String,  serverip String,  time Float64,  to String,  to_port String,  uniqno String,  recdate Date MATERIALIZED toDate(time)) ENGINE = MergeTree(recdate, (recdate, serverip), 8192)


('INSERT INTO middle_call (domain,from_port,from,serverip,uniqno,time,event) VALUES', [('siptalk64.xcastlabs.com', '16462', '75.145.154.225', '10.10.10.62', '199848', 1517865917.533766, 'CLN_AUDIO')])
('INSERT INTO middle_call (domain,direction,serverip,uniqno,time,event) VALUES', [('siptalk64.xcastlabs.com', 'CLN', '10.10.10.62', '199848', 1517865918.903629, 'BYE')])
('INSERT INTO middle_call (domain,from,direction,serverip,uniqno,to,time,event) VALUES', [('siptalk64.xcastlabs.com', '7065D06L01', 'CLN', '10.10.10.62', '199849', 'pickup', 1517865922.851535, 'INVITE')])
('INSERT INTO middle_call (domain,from,direction,serverip,uniqno,to,time,event) VALUES', [('siptalk64.xcastlabs.com', '7065D06L01', 'CLN', '10.10.10.62', '199849', 'pickup', 1517865922.987284, 'INVITE')])
('INSERT INTO middle_call (domain,serverip,uniqno,fmode,time,event) VALUES', [('siptalk64.xcastlabs.com', '10.10.10.62', '199849', 'C', 1517865923.170639, 'TALK')])
('INSERT INTO middle_call (domain,from_port,from,serverip,uniqno,time,event) VALUES', [('siptalk64.xcastlabs.com', '16464', '75.145.154.225', '10.10.10.62', '199849', 1517865923.172043, 'CLN_AUDIO')])
('INSERT INTO middle_call (domain,from_port,from,serverip,uniqno,time,event) VALUES', [('siptalk64.xcastlabs.com', '45120', '75.145.154.234', '10.10.10.62', '199849', 1517865923.208256, 'SRV_AUDIO')])
('INSERT INTO middle_call (domain,from,direction,serverip,uniqno,to,time,event) VALUES', [('siptalk64.xcastlabs.com', '7065D06L01', 'CLN', '10.10.10.62', '199850', '6065*siptalk64.xcastlabs.com-75.145.154.225+45062', 1517865923.577075, 'INVITE')])
('INSERT INTO middle_call (domain,from,direction,serverip,uniqno,to,time,event) VALUES', [('siptalk64.xcastlabs.com', '7065D06L01', 'CLN', '10.10.10.62', '199850', '6065*siptalk64.xcastlabs.com-75.145.154.225+45062', 1517865923.634572, 'INVITE')])
('INSERT INTO middle_call (domain,serverip,uniqno,fmode,time,event) VALUES', [('siptalk64.xcastlabs.com', '10.10.10.62', '199850', '=', 1517865923.922403, 'TALK')])
('INSERT INTO middle_call (domain,direction,serverip,uniqno,time,event) VALUES', [('siptalk64.xcastlabs.com', 'SRV', '10.10.10.62', '199849', 1517865925.350218, 'BYE')])
('INSERT INTO middle_call (domain,direction,serverip,uniqno,time,event) VALUES', [('siptalk64.xcastlabs.com', 'CLN', '10.10.10.62', '199850', 1517865932.810739, 'BYE')])
('INSERT INTO middle_registration (domain,callid,intip,agent,serverip,aor,time,line,extip,event) VALUES', [('siptalk64.xcastlabs.com', '4cf6868eaf9a26a@10.10.8.10', '10.10.8.10', 'Htek UC840 V1.0.4.2.11', '10.10.10.62', 'sip:UC8xx-0001-01*siptalk64.xcastlabs.com-75.145.154.225+5260@75.145.154.234:7064', 1517865937.676542, 'UC8xx-0001-01', '75.145.154.225', 'REG')])
('INSERT INTO middle_call (uniqno,domain,event,serverip,time) VALUES', [('199847', 'siptalk64.xcastlabs.com', 'DTOR', '10.10.10.62', 1517865957.193561)])
('INSERT INTO middle_call (uniqno,domain,event,serverip,time) VALUES', [('199848', 'siptalk64.xcastlabs.com', 'DTOR', '10.10.10.62', 1517865958.903931)])
('INSERT INTO middle_call (uniqno,domain,event,serverip,time) VALUES', [('199849', 'siptalk64.xcastlabs.com', 'DTOR', '10.10.10.62', 1517865965.349911)])
('INSERT INTO middle_call (uniqno,domain,event,serverip,time) VALUES', [('199850', 'siptalk64.xcastlabs.com', 'DTOR', '10.10.10.62', 1517865972.811123)])
('INSERT INTO middle_active (full,dialogs,calls,extra,started,regs,serverip,time,event) VALUES', [('0', '1', '0', 'R:19', '1516742939', '19', '10.10.10.62', 1517866139.374878, 'ACTIVE')])
('INSERT INTO middle_registration (domain,callid,intip,agent,serverip,aor,time,line,extip,event) VALUES', [('russ.xcastlabs.com', '5326ef0a-c226ff31@10.0.0.207', '10.0.0.207', 'Linksys/SPA1001-3.1.19(SE)', '10.10.10.62', 'sip:312D01L01*russ.xcastlabs.com-67.167.37.164+16195@75.145.154.234:7064', 1517866325.599466, '312D01L01', '67.167.37.164', 'REG')])
('INSERT INTO middle_registration (domain,callid,intip,agent,serverip,aor,time,line,extip,event) VALUES', [('siptalk64.xcastlabs.com', '9371923e738ab3c4', '10.10.10.55', 'baresip v0.4.20 (x86_64/linux)', '10.10.10.62', 'sip:SPA942-0001-02-0x22e53f0*siptalk64.xcastlabs.com-75.145.154.225+33326@75.145.154.234:7064', 1517866360.165728, 'SPA942-0001-02-0x22e53f0', '75.145.154.225', 'REG')])
('INSERT INTO middle_active (full,dialogs,calls,extra,started,regs,serverip,time,event) VALUES', [('0', '0', '0', 'R:19', '1516742939', '19', '10.10.10.62', 1517866739.373903, 'ACTIVE')])
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
non_string_fields={'time':'Float64','Time':'Float64'}
fields_with_ports=['from','to']


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

tables={
    "call":         ['event','time','serverip','uniqno','domain','direction','from','from_port','to','to_port','extra','fmode'],
    "registration": ['event','time','serverip','domain','callid','intip','agent','aor','line','extip','reason'],
    "active":       ['event','time','serverip','full','dialogs','calls','extra','started','regs']
    }

class xcast_event_table:

    def print_table(self,table_name):
        if self.table_name in xcast_event_tables:
            return(self.create_new_table)

    def __init__(self,record,ev_type,table_name_prefix,even_if_exists=False):
        #print(record,ev_type,table_name_prefix,even_if_exists)
        if ev_type.lower() in ['active',] : table_name = "active"
        elif ev_type.lower() in ['invite','timeout','bye','cancel','talk', 'dtor','reject','srv_audio','cln_audio','srv_video','cln_video'] : table_name = "call"
        elif ev_type.lower() in ['reg','unreg','faild'] : table_name = "registration"
        else: raise SystemExit
        self.table_name=table_name_prefix+table_name
        #print(ev_type,self.table_name,even_if_exists)
        if( self.table_name in xcast_event_tables):
            self.create_new_table=''
            pass
        else:
            drop_old_table="DROP TABLE IF EXISTS {};".format(self.table_name)
            other_fields=''
            create_even_if_exists= ("IF NOT EXISTS ",drop_old_table) [even_if_exists]
            for key in sorted(tables[table_name]):
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
""".format(create_even_if_exists, self.table_name, other_fields)
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
        while client:
            record=q.get()
            if(record):
                #create_table.print_tables()
                ev_type=record["Event"]
                #table_name='middle_events_'+ev_type.lower()
                
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

                try:
                    if(len(record_values)>0):
                        event_processor=xcast_event_table(record,ev_type,'middle_')
                        if event_processor:
                            table_name= event_processor.table_name
                            create_table=event_processor.print_table(table_name)#.encode('utf-8')
                            if(create_table):
                                #print(create_table)
                                r =client.execute(create_table)
                                time.sleep(2)
                                if r:print(r)
                        query="""INSERT INTO {} ({}) VALUES""".format(table_name,field_names)#.encode('utf-8')
                        print(query,[record_values])
                        r=client.execute(query,[record_values],types_check=True)
                        if r:print(r)
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
    for i in range(1):
        worker = Thread(target=prepare_insert_query, args=(events_q,client))
        worker.setDaemon(True)
        worker.start()
    for i in range(8):
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
