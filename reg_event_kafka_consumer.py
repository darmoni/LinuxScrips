#!/usr/bin/env python

def usage():
    print('~/Downloads/kafka_2.11-1.0.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic my-replicated-topic | reg_event_kafka_consumer.py')

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
'''
xcast_event_tables={}
non_string_fields={'time':'Float64','Time':'Float64'}
fields_with_ports=['from','to']

Event: INVITE\nUniqNo: 311363\nDomain: siptalk64.xcastlabs.com\nDirection: CLN\nFrom: UC8xx-0001-01\nTo: 98563\nTime: 1518186873.736757994\nServerIP: 10.10.10.62
Event: INVITE\nUniqNo: 311363\nDomain: siptalk64.xcastlabs.com\nDirection: CLN\nFrom: UC8xx-0001-01\nTo: 98563\nTime: 1518186873.786770105\nServerIP: 10.10.10.62
Event: REJECT\nUniqNo: 311363\nDomain: siptalk64.xcastlabs.com\nExtra: 408,Request TimeoutTime: 1518186876.922652960\nServerIP: 10.10.10.62
Event: DTOR\nUniqNo: 311363\nDomain: siptalk64.xcastlabs.com\nTime: 1518186916.922527075\nServerIP: 10.10.10.62
('INSERT INTO middle_call (domain,from,direction,serverip,uniqno,to,time,event) VALUES', [('siptalk64.xcastlabs.com', 'UC8xx-0001-01', 'CLN', '10.10.10.62', '311363', '98563', 1518186873.736758, 'INVITE')])
('INSERT INTO middle_call (domain,from,direction,serverip,uniqno,to,time,event) VALUES', [('siptalk64.xcastlabs.com', 'UC8xx-0001-01', 'CLN', '10.10.10.62', '311363', '98563', 1518186873.78677, 'INVITE')])
('INSERT INTO middle_call (uniqno,domain,event,serverip,extra) VALUES', [('311363', 'siptalk64.xcastlabs.com', 'REJECT', '10.10.10.62', '408,Request TimeoutTime: 1518186876.922652960')])
<class 'clickhouse_driver.errors.ServerException'>
()
Code: 47.
DB::Exception: Unknown identifier: time. Stack trace:

0. /usr/bin/clickhouse-server(StackTrace::StackTrace()+0x15) [0x70bf765]
1. /usr/bin/clickhouse-server(DB::Exception::Exception(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int)+0x1e) [0x191f92e]
2. /usr/bin/clickhouse-server(DB::ExpressionAnalyzer::getActionsImpl(std::shared_ptr<DB::IAST> const&, bool, bool, DB::ExpressionAnalyzer::ScopeStack&)+0x24b3) [0x6a4c7f3]
3. /usr/bin/clickhouse-server() [0x6a4d390]
4. /usr/bin/clickhouse-server(DB::ExpressionAnalyzer::getActions(bool)+0x285) [0x6a51075]
5. /usr/bin/clickhouse-server(DB::evaluateMissingDefaults(DB::Block&, DB::NamesAndTypesList const&, std::unordered_map<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, DB::ColumnDefault, std::hash<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >, std::equal_to<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >, std::allocator<std::pair<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const, DB::ColumnDefault> > > const&, DB::Context const&)+0x840) [0x6a760b0]
6. /usr/bin/clickhouse-server(DB::AddingDefaultBlockOutputStream::write(DB::Block const&)+0x2a8) [0x68d0658]
7. /usr/bin/clickhouse-server(DB::ProhibitColumnsBlockOutputStream::write(DB::Block const&)+0x5e) [0x6965a5e]
8. /usr/bin/clickhouse-server(DB::SquashingBlockOutputStream::finalize()+0x255) [0x696e9e5]
9. /usr/bin/clickhouse-server(DB::SquashingBlockOutputStream::writeSuffix()+0x10) [0x696ec50]
10. /usr/bin/clickhouse-server(DB::TCPHandler::processInsertQuery(DB::Settings const&)+0x331) [0x192e7b1]
11. /usr/bin/clickhouse-server(DB::TCPHandler::runImpl()+0x44b) [0x192eccb]
12. /usr/bin/clickhouse-server(DB::TCPHandler::run()+0x2a) [0x192f9fa]
13. /usr/bin/clickhouse-server(Poco::Net::TCPServerConnection::start()+0xe) [0x73cb2ae]
14. /usr/bin/clickhouse-server(Poco::Net::TCPServerDispatcher::run()+0x165) [0x73cb675]
15. /usr/bin/clickhouse-server(Poco::PooledThread::run()+0x76) [0x718c656]
16. /usr/bin/clickhouse-server(Poco::ThreadImpl::runnableEntry(void*)+0x37) [0x7188647]
17. /usr/bin/clickhouse-server() [0x74abb8e]
18. /lib/x86_64-linux-gnu/libpthread.so.0(+0x76b9) [0x7efe6f3eb6b9]
19. /lib/x86_64-linux-gnu/libc.so.6(clone+0x6c) [0x7efe6ec1441c]

/home/nir/bin/reg_event_kafka_consumer.py Oops
^Cgot sig(2)


'''
from middle_event_structure import Xcast_event_table, translate_field, separate_addr_port
#import middle_event_structure

def to_db(line,q):
    #print(line)
    parts=line.replace("\\n","\n").split("\n")
    #print(parts)
    if(len(parts)< 1):
        return None
    if('Event' != parts[0].strip().split(": ")[0]):
        print(parts[0].strip().split(": ")[0])
        return None
    
    #print(parts)
    fields={}
    for f in parts:
        legal_field=f.find(": ")
        value_pos = legal_field+2
        if(0 < legal_field):
            key = f[:legal_field]
            value = f[value_pos:]
            #key, value = f.split(": ")
            if not separate_addr_port(key, value,fields):
                fields[key.strip()] = value.strip()
    #print(fields)
    q.put(fields)

def prepare_insert_query(q,client):
    try:
        if not q:
            print("There is no Queue")
        if not client:
            print("There is no client")
        if not client:
            safe_exit()
        while client:
            record=q.get()
            if(record):
                #print(record)
                #create_table.print_tables()
                ev_type=record["Event"]
                #table_name='middle_events_'+ev_type.lower()
                if('Time' not in record):
                    print('ERROR: There if no time field in the record !!!: {}\n Fixing it locally'.format(record))
                    record["Time"]=  "{:18.9f}".format(time.time())
                    #continue
                field_names=(",".join(record.keys())).lower()
                record_values=[]
                for k in record.keys():
                    if (k in Xcast_event_table.non_string_fields):
                        value = translate_field(Xcast_event_table.non_string_fields[k],record[k])
                    else:
                        value = str(record[k])
                    record_values.append(value)
                record_values=tuple(record_values)
                #field_values=",".join(record_values)

                try:
                    if(len(record_values)>0):
                        event_processor=Xcast_event_table(record,ev_type,'middle_')
                        if event_processor:
                            table_name= event_processor.table_name
                            create_table=event_processor.print_table(table_name)#.encode('utf-8')
                            if(create_table):
                                #print(create_table)
                                r =client.execute(create_table)
                                time.sleep(0.2)
                                if r:print(r)
                        query="""INSERT INTO {} ({}) VALUES""".format(table_name,field_names)#.encode('utf-8')
                        #print(query,[record_values])
                        r=client.execute(query,[record_values],types_check=True)
                        if r:print(r)
                except Exception as inst:
                    print type(inst)
                    print inst.args
                    print inst
                    print __file__, 'Oops'
            #del record
                q.task_done()
            else:
                print("there is no record")
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
            time.sleep(0.1)

def read_from_stdin(events_q):
    while True:
        data=sys.stdin.readline().strip()
        if(data and len(data)>1):
            #print(data)
            to_db(data,events_q)
        elif(data):
            continue
        else:
            time.sleep(0.1)


def collect_middle_events(client):
    #sock = socket(AF_INET,SOCK_DGRAM)
    #sock.bind(('',32802))
    #msg = "Hello UDP server"
    events_q = Queue(maxsize=0)
    #db_cmd_q = Queue(maxsize=0)
    for i in range(1):
        worker = Thread(target=prepare_insert_query, args=(events_q,client))
        worker.setDaemon(True)
        worker.start()
    for i in range(1):
        middle_worker = Thread(target=read_from_stdin, args=(events_q,))
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
