#!/usr/bin/env python

from middle_event_structure import Xcast_event_table, translate_field, separate_addr_port
from Queue import Queue, Empty
import ConfigParser as configparser
import sys,signal, time
from threading import Thread

def to_db(line,q):
    print(line)
    parts=line.replace("\\n","\n").split("\n")
    print(parts)
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
    print(fields)
    q.put(fields)

def safe_exit():
    sys.exit(-1)

def prepare_insert_query(q,topic=None):
    try:
        if not q:
            print("There is no Queue")
            safe_exit()
        record=q.get()
        if(record):
            ev_type=record["Event"]
            record["Time"]=record.setdefault("Time", "{:18.9f}".format(time.time()))
            print(record)
            event_processor=Xcast_event_table(record,ev_type,'')
            if event_processor:
                table_name= event_processor.table_name
                #print(sorted(Xcast_event_table.tables[table_name]))
                #field_names=(",".join(record.keys())).lower()
                record_values={}
                table_values=[]
                for k in record:
                    if 'dos' == table_name and 'shield' == k.lower():
                        print ("{}->{}").format(k, record[k])
                        shield_value = ('0','1')[record[k] == 'On']
                        print ("{}->{}").format(k.lower(), shield_value)
                        record_values.update({k.lower(): shield_value})
                    else:
                        record_values.update({k.lower(): record[k]})
                counter=0
                for k in sorted(Xcast_event_table.tables[table_name]):
                    print(table_name,k)
                    table_values.append(record_values.setdefault(k,"\N"))
                    print(counter,table_values[counter])
                    counter += 1
                read_topic = 'middle_'+table_name
                fields= "\t".join(table_values)+"\n"
                print(read_topic, fields)
                if(topics and read_topic not in topics):
                    pass
                    #producer.send(topic, fields)
                #else:
                #    producer.send(read_topic, fields)
                del event_processor
                q.task_done()
            else:
                print("could not create Xcast_event_table\n")
                safe_exit()
        else:
            print("there is no record")
    except Exception as inst:
        print (type(inst))
        print (inst.args)
        print (inst)
        print (__file__, 'Oops')

def dummy_dos(events_q, topic='middle_dos'):
    while True:
        event='DDOS'
        #ip= '75.145.154.225'
        #port=45162
        serverip='dummy_dos.nowhere.mars'
        shield='Off'
        timestamp="{:18.9f}".format(time.time())
        message="Event: {}\nShield: {}\nTime: {}\nserverip: {}".format(event,shield,timestamp,serverip)
        #print (message)
        #print (repr(message))
        to_db(message,events_q)
        time.sleep(3)

def collect_middle_events(topic):
    events_q = Queue(maxsize=0)
    for i in range(1):
        worker = Thread(target=prepare_insert_query, args=(events_q,topic))
        worker.setDaemon(True)
        worker.start()
    for i in range(1):
        middle_worker = Thread(target=dummy_dos, args=(events_q,'middle_dos'))
        middle_worker.setDaemon(True)
        middle_worker.start()

    while True:
            time.sleep(2)

if __name__ == '__main__':
    file_config = configparser.ConfigParser()
    file_config.read(['middle_producer_setup.cfg'])
    #log.configure(file_config.get('log', 'level'))

    cfg_bootstrap_servers = file_config.get('producer', 'bootstrap_servers')
    if (cfg_bootstrap_servers):
        bootstrap_servers = cfg_bootstrap_servers.split(", ")
    #print (bootstrap_servers)
    security_protocol = file_config.get('access', 'security_protocol')
    if('SASL_PLAINTEXT'== security_protocol):
        sasl_mechanism= file_config.get('access', 'sasl_mechanism')
        user = file_config.get('access', 'sasl_plain_username')
        password = file_config.get('access', 'sasl_plain_password')
    compression = file_config.get('access', 'compression') 
    testing_topic = file_config.get('access', 'testing_topic')
    topics= file_config.get('access', 'topics')
    print("topics: {}\n".format(topics))
    #print("NOT ready to produce topic {}\n".format(topic))
    #producer = KafkaProducer(client_id=client_id, compression_type=compression, bootstrap_servers=bootstrap_servers, security_protocol=security_protocol, sasl_mechanism=sasl_mechanism, sasl_plain_username=user,sasl_plain_password=password)
    print("ready to produce topic {}\n".format(testing_topic))
    try:
        collect_middle_events(topics)
    except Exception as inst:
        print (type(inst))
        print (inst.args)
        print (inst)
        print (__file__, 'Oops')
        safe_exit()
    safe_exit()
