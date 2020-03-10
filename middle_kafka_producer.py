#!/usr/bin/env python2

ID='$Id$'.replace(' $','').replace('$','')
DATE='$Date$'.replace('$','')

#File name "middle_kafka_producer.py"

import resource
from kafka import KafkaProducer
import sys
import signal, time
from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import os.path
import json, syslog, argparse

from middle_event_structure import Xcast_event_table, translate_field, separate_addr_port, ID as middle_event_structure_ID, DATE as middle_event_structure_DATE
if (sys.version_info < (3, 0)):
    import ConfigParser as configparser
    from Queue import Queue, Empty
    #import queue
else:
    import configparser
    import queue

MAX_SIZE=4096
if (sys.version_info < (3, 0)):
    client_id='XCASTLABS_events_capture_and_producer'
else:
    client_id='XCASTLABS.p3_events_capture_and_producer'

syslog_priorities = {
    "EMERG": syslog.LOG_EMERG,
    "ALERT": syslog.LOG_ALERT,
    "CRIT": syslog.LOG_CRIT,
    "ERR": syslog.LOG_ERR,
    "WARNING": syslog.LOG_WARNING,
    "NOTICE": syslog.LOG_NOTICE,
    "INFO": syslog.LOG_INFO,
    "DEBUG": syslog.LOG_DEBUG
}
use_syslog=False
resources=[]
max_resources_size = len(resources)
read_from_middle_counter = 0
prepare_insert_query_counter = 0
producer_counter = 0
ru_maxrss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
current_ru_maxrss = ru_maxrss

def safe_exit():
    print ("safe_exit initial size = {}\n".format(len(resources)))
    counter=0
    for r in resources:
        print ("deleting {}\n".format(counter))
        del resources[counter]
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

#TYPE_RAW = 10
TYPE_SUM =  0
TYPE_AVG =  1
TYPE_MIN =  2
TYPE_MAX =  3
#{"Event":"STAT","ExtProc":"73,1","IntProc":"0,0","MaxQueueSize":"1,4","Method":"SUBSCRIBE:3","Self":"75.145.154.234:7060","event_timestamp":"1555513888.357527971"}
def serialize_stat(sock, record, address = '', port = 3666, my_component_name = "Middle"):
    buf_template = "{},{},{},{}".format('{}', my_component_name, 'Stat','{}')+",{},{},{}"

    try:
        #print(type(record))
        #record = json_fields
        fields = {}
        for k in record.keys():
            #print('{} ==> {}'.format(k, record[k]))
            if 'event_timestamp' == k:
                #fields[k] = record[k]
                continue
            elif 'Self' == k:
                NodeName = record[k]
                continue
            elif 'ExtProc' == k or 'IntProc' == k:
                subComp = k
                [counter, time] = record[k].split(',')
                buf = buf_template.format('Self', subComp, "NumberOfSipMessages", 'TYPE_SUM', 'StatBlock.d.nmbExtProc').encode('utf-8')
                if 'IntProc' == k:
                    buf.replace('ExtProc','IntProc')
                syslog.syslog(syslog.LOG_DEBUG, buf)
                buf = buf_template.format('Self', subComp, "MaxProcessingTime", 'TYPE_MAX', 'StatBlock.d.maxExtProc').encode('utf-8')
                if 'IntProc' == k:
                    buf.replace('ExtProc','IntProc')
                syslog.syslog(syslog.LOG_DEBUG, buf)

                fields['{}{}'.format(subComp,'NumberOfSipMessages')] = [subComp, TYPE_SUM, counter]
                fields['{}{}'.format(subComp,'MaxProcessingTime')] = [subComp, TYPE_MAX, time]
                continue
            elif 'MaxQueueSize' == k:
                subComp = 'Queue'
                buf = buf_template.format('Self', subComp, "NumberOfBlocks", 'TYPE_MAX', 'StatBlock.d.maxBlkInQ').encode('utf-8')
                syslog.syslog(syslog.LOG_DEBUG, buf)
                [counter, threads] = record[k].split(',')
                buf = buf_template.format('Self', subComp, "MaxThreads", 'TYPE_MAX', 'StatBlock.d.maxThreads').encode('utf-8')
                syslog.syslog(syslog.LOG_DEBUG, buf)
                fields['{}{}'.format(subComp, 'NumberOfBlocks')] = [subComp, TYPE_MAX, counter]
                fields['{}{}'.format(subComp, 'MaxThreads')] = [subComp, TYPE_MAX, threads]
                continue
            elif 'Method' == k:
                subComp = k
                parts = record[k].split(',')
                for method in parts:
                    [name, count] = method.split(':')
                    fieldName = "{}NumberOf'{}'s".format(subComp, name.capitalize())
                    fields[fieldName] = [subComp, TYPE_SUM, count]
                    buf = buf_template.format('Self', subComp, fieldName.replace(subComp,''), 'TYPE_MAX', 'StatBlock.Methods[method]').encode('utf-8')
                    syslog.syslog(syslog.LOG_DEBUG, buf)
                continue
            elif 'Bounce' == k:
                subComp = k
                parts = record[k].split(',')
                for ResponseCode in parts:
                    [name, count] = ResponseCode.split(':')
                    fieldName = '{}NumberOf{}s'.format(subComp, name.capitalize())
                    fields[fieldName] = [subComp, TYPE_SUM, count]
                    buf = buf_template.format('Self', subComp, fieldName.replace(subComp,''), 'TYPE_MAX', 'StatBlock.Bounces[ResponseCode]').encode('utf-8')
                    syslog.syslog(syslog.LOG_DEBUG, buf)
                continue
            elif 'BadEvent' == k:
                subComp = k
                parts = record[k].split(',')
                for EventType in parts:
                    [name, count] = EventType.split(':')
                    fieldName = '{}NumberOf{}s'.format(subComp, name.capitalize())
                    fields[fieldName] = [subComp, TYPE_SUM, count]
                    buf = buf_template.format('Self', subComp, fieldName.replace(subComp,''), 'TYPE_MAX', 'StatBlock.BadEvents[EventType]').encode('utf-8')
                    syslog.syslog(syslog.LOG_DEBUG, buf)
                continue
            elif 'Dos' == k:
                subComp = k
                parts = record[k].split(',')
                for DosType in parts:
                    [name, count] = DosType.split(':')
                    fieldName = '{}NumberOf DosType-{}s'.format(subComp, name.capitalize())
                    fields[fieldName] = [subComp, TYPE_SUM, count]
                    buf = buf_template.format('Self', subComp, fieldName.replace(subComp,''), 'TYPE_MAX', 'StatBlock.DOSs[DosType]').encode('utf-8')
                    syslog.syslog(syslog.LOG_DEBUG, buf)
                continue

        for k in sorted(fields.keys()):
            subComp = fields[k][0]
            name = k.replace(subComp,'')
            buf = buf_template.format(NodeName, subComp, name, fields[k][1], fields[k][2]).encode('utf-8')
            #print(record['event_timestamp'].encode('utf-8'), buf)
            syslog.syslog(syslog.LOG_DEBUG, buf)
            #print("serialize_stat sock.sendto('{}', ({},{}))".format(buf, address, port))
            sock.sendto(buf, (address, port))
        syslog.syslog(syslog.LOG_DEBUG, json.dumps(record, separators=(',',':'), sort_keys=True))

    except Exception as inst:
        messages = ["Exception", "{}".format(type(inst)), "{}".format(inst.args), "{}".format(inst), "{} {}".format(__file__, 'serialize_stat Oops')]
        for i in range(len(messages)):
            oops = messages[i]
            print(oops)
            syslog.syslog(syslog.LOG_CRIT, oops)
        safe_exit()

def my_stat_producer(metricsServer, q, printer_q):
    ''' PHP reference
            $buf = $this->serverNode . ',' . $this->serviceName . ",$component, $subComponent, $field, $type, $value";
            socket_sendto($this->STATSOCKET, $buf, strlen($buf), 0, $this->metricCollectorIP, $this->metricCollectorPort);
    python sending to port refrence
        PORT = port
        sock = socket(AF_INET,SOCK_DGRAM)
        for counter in range(0, count):
            #print(msg)
            sock.sendto(msg.encode('utf-8'),(address, PORT))

    '''

    try:
        #print(metricsServer)
        address = metricsServer['address']
        port = metricsServer['port']
        sock = socket(AF_INET,SOCK_DGRAM)
        while(q):
            if time_to_go():
                break
            (event,record) = q.get()
            serialize_stat(sock, record, address, port, 'middle')
            q.task_done()
            #print("my_stat_producer '{} {}'".format(event, record))

    except Exception as inst:
        if q: q.task_done()
        messages = ["Exception: Can't send to stat_producer", "{}".format(type(inst)), "{}".format(inst.args), "{}".format(inst), "{} {}".format(__file__, 'my_stat_producer Oops')]
        for i in range(len(messages)):
            oops = messages[i]
            print(oops)
            syslog.syslog(syslog.LOG_CRIT, oops)
    safe_exit()


def my_producer(producer, q, printer = None):
    global producer_counter
    if None == q:
        messages = ["my_producer: There is no Queue",]
        for i in range(len(messages)):
            oops = messages[i]
            print(oops)
            syslog.syslog(syslog.LOG_CRIT, oops)
        safe_exit()
    if None == producer:
        messages = ["my_producer: There is no producer",]
        for i in range(len(messages)):
            oops = messages[i]
            print(oops)
            syslog.syslog(syslog.LOG_CRIT, oops)
        safe_exit()
    producer_counter_units = 100000
    print("my_producer listening, counter = {}".format(producer_counter))
    while producer:
        if time_to_go():
            break
        try:
            (topic,record)=q.get()
            #print(topic,record)
            producer_counter += 1
            #if producer_counter >= producer_counter_units:
                #pass
                #producer_counter = 0;
                #if printer: printer.put((topic,record))
            if len(topic) > 0:
                producer.send(topic,record)
                #print("my_producer listening, counter = {}".format(producer_counter))
            q.task_done()
        except KafkaTimeoutError:
            if q: q.task_done()
            messages = ["Exception: KafkaTimeoutError", "{}".format(type(inst)), "{}".format(inst.args), "{}".format(inst), "{} {}".format(__file__, 'my_producer Oops')]
            for i in range(len(messages)):
                oops = messages[i]
                print(oops)
                syslog.syslog(syslog.LOG_CRIT, oops)
            break
        except Exception as inst:
            if q: q.task_done()
            messages = ["Exception: Can't send to producer", "{}".format(type(inst)), "{}".format(inst.args), "{}".format(inst), "{} {}".format(__file__, 'my_producer Oops')]
            for i in range(len(messages)):
                oops = messages[i]
                print(oops)
                syslog.syslog(syslog.LOG_CRIT, oops)
            break
    safe_exit()

periodic_print_template_deltas =    "Max Memory usage = {} (kb), delta  input_counter = {}, delta  mid_queue_counter = {}, delta  to_kafka_counter = {} live threads = {}\n"
periodic_print_template =           "Max Memory usage = {} (kb), actual input_counter = {}, actual mid_queue_counter = {}, actual to_kafka_counter = {} live threads = {}\n"
periodic_printer_template = "printer counter = {}, input_counter = {}, mid_queue_counter = {}\n"


class PeriodicReporter:
    global read_from_middle_counter, prepare_insert_query_counter, producer_counter, periodic_printer_template, current_ru_maxrss, ru_maxrss, use_syslog
    def __init__(self, name = 'main loop'):
        self.name = name
        self.refresh()
        #self.last_read_from_middle_counter=read_from_middle_counter
        #self.last_prepare_insert_query_counter = prepare_insert_query_counter
        #self.last_producer_counter = producer_counter

    def refresh(self):
        self.last_read_from_middle_counter=read_from_middle_counter
        self.last_prepare_insert_query_counter = prepare_insert_query_counter
        self.last_producer_counter = producer_counter

    def report(self):
        try:
            deltas = {}
            deltas.update({'delta input_counter': read_from_middle_counter - self.last_read_from_middle_counter})
            deltas.update({'delta mid_queue_counter': prepare_insert_query_counter - self.last_prepare_insert_query_counter})
            deltas.update({'delta to_kafka_counter': producer_counter - self.last_producer_counter})
            self.refresh()
            actuals = {}
            actuals.update({'input_counter': self.last_read_from_middle_counter})
            actuals.update({'mid_queue_counter': self.last_prepare_insert_query_counter})
            actuals.update({'to_kafka_counter': self.last_producer_counter})
            #delta_data="DEBUG Using Dict for printing: {}\n".format(json.dumps(deltas), separators=(',', ':'), sort_keys=True)
            delta_data="{} {}\n".format(self.name, periodic_print_template_deltas.strip().format(ru_maxrss, deltas['delta input_counter'], deltas['delta mid_queue_counter'], deltas['delta to_kafka_counter'], len(resources)))
            syslog.syslog(syslog.LOG_ERR, delta_data)
            data="{} {}\n".format(self.name, periodic_print_template.strip().format(ru_maxrss, self.last_read_from_middle_counter, self.last_prepare_insert_query_counter, self.last_producer_counter, len(resources)))
            actual_values = []
            for a in actuals:
                actual_values.append(actuals[a])
            d_max = max(actual_values)
            d_min = min(actual_values)
            if d_min < d_max:
                minmax = "NOTE: Min Delta {} <> Max Delta {} !!!".format(d_min, d_max)
                #print(minmax)
                syslog.syslog(syslog.LOG_ERR,minmax)
            if use_syslog:
                syslog.syslog(syslog.LOG_ERR, data)
        except Exception as inst:
            messages = ["{}".format(type(inst)), "{}".format(inst.args), "{}".format(inst), "{} {}".format(__file__, 'PeriodicReporter.report() Oops')]
            for i in range(len(messages)):
                oops = messages[i]
                print(oops)
                syslog.syslog(syslog.LOG_CRIT, oops)
            safe_exit()


def sample_memory_usage(who_is_asking = ''):
    global current_ru_maxrss, ru_maxrss, use_syslog
    try:
        ru_maxrss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if ru_maxrss > current_ru_maxrss:
            current_ru_maxrss = ru_maxrss
            oops='{} Max Memory usage: {} (kb)\n'.format(who_is_asking, current_ru_maxrss)
            print(oops)
            if use_syslog:
                syslog.syslog(syslog.LOG_ERR, oops)
    except:
        pass

def my_std_printer(q):
    global read_from_middle_counter, prepare_insert_query_counter, producer_counter, periodic_printer_template
    try:
        counter = 0;
        print(periodic_printer_template.format(counter, read_from_middle_counter, prepare_insert_query_counter))
        #use_syslog = False
        if None == q:
            messages = ["There is no Queue", "Can't send to printer", "Exiting"]
            for i in range(len(messages)):
                oops = messages[i]
                if use_syslog:
                    syslog.syslog(syslog.LOG_CRIT, oops)
                print(oops)
            safe_exit()
        print('{} Processing started. use_syslog = {}'.format(client_id, use_syslog))
        while True:
            if time_to_go():
                break
            record=q.get()
            #break # DEBUG
            if(record):
                counter += 1
                #DEBUG print("{}\n".format(json.dumps(record)))
            q.task_done()
            if 0 == counter % 1000:
                print(periodic_printer_template.format(counter, read_from_middle_counter, prepare_insert_query_counter))
                counter = 0
        safe_exit()
    except Exception as inst:
        messages = ["my_std_printer", "{}".format(type(inst)), "{}".format(inst.args), "{}".format(inst), "{} {}".format(__file__, 'my_std_printer Oops')]
        for i in range(len(messages)):
            oops = messages[i]
            syslog.syslog(syslog.LOG_CRIT, oops)
            print(oops)
    safe_exit()


def my_syslog_printer(q):
    global read_from_middle_counter, prepare_insert_query_counter, periodic_printer_template
    counter = 0
    use_syslog = True
    try:
        print('{} Processing started. use_syslog = {}'.format(client_id, use_syslog))
        syslog.syslog(syslog.LOG_ERR, periodic_printer_template.format(counter, read_from_middle_counter, prepare_insert_query_counter))
        if None == q:
            messages = ["There is no Queue", "Can't send to printer", "Exiting"]
            for i in range(len(messages)):
                oops = messages[i]
                if use_syslog:
                    syslog.syslog(syslog.LOG_CRIT, oops)
                print(oops)
            safe_exit()
        message = '{} Processing started. use_syslog = {}'.format(client_id, use_syslog)
        syslog.syslog(syslog.LOG_ERR, message)
        #print(message)
        if use_syslog:
            while True:
                if time_to_go():
                    break
                record=q.get()
                #break # DEBUG
                if(record):
                    counter += 1
                    #syslog.syslog(syslog.LOG_DEBUG, "{}\n".format(json.dumps(record, separators=(",",":"))))
                q.task_done()
                if 0 == counter % 1000:
                    syslog.syslog(syslog.LOG_ERR, periodic_printer_template.format(counter, read_from_middle_counter, prepare_insert_query_counter))
                    counter = 0
            safe_exit()
    except Exception as inst:
        messages = ["my_syslog_printer oops", "{}".format(type(inst)), "{}".format(inst.args), "{}".format(inst), "{} {}".format(__file__, 'my_syslog_printer Exiting')]
        for i in range(len(messages)):
            oops = messages[i]
            syslog.syslog(syslog.LOG_CRIT, oops)
            print(oops)
    safe_exit()

def to_db(line, q):
    #print(line)
    parts=line.replace("\\n","\n").split("\n")
    #print(parts)
    if(len(parts)< 1):
        return None
    if('Event' != parts[0].strip().split(": ")[0]):
        #print(parts[0].strip().split(": ")[0])
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

def dummy_active(producer,topic='middle_active'):
    record={}
    while producer:
        record['calls']='89'
        record['dialogs']='64'
        record['event']="ACTIVE"
        record['extra']="R:22"
        record['full_mode']='23'
        record['registrations']='22'
        record['sbc_ip']='dummy_active.nowhere.mars'
        record['started_timestamp']='1521757433'
        record['event_timestamp']="{:18.9f}".format(time.time())
        message = json.dumps(record, separators=(',',':'), sort_keys=True)
        #print (message)
        #time.sleep(3)
        #print (repr(message))
        #continue
        metrics = producer.send(topic,message)
        if (metrics):
            print ("key = {}\n".format(metrics.get()))
        time.sleep(3)

def dummy_dos(producer, topic='middle_dos'):
    record={}
    while producer:

        record['event']='BLOCK'
        record['ip']= '75.145.154.225'
        record['port']=45162
        record['sbc_ip']='dummy_dos.nowhere.mars'
        record['blocked']='0'
        record['event_timestamp']="{:18.9f}".format(time.time())
        message = json.dumps(record, separators=(',',':'), sort_keys=True)
        print (message)
        print (repr(message))
        #time.sleep(3)
        #continue
        metrics = producer.send(topic,message)
        if (metrics):
            print ("key = {}\n".format(metrics.get()))
        time.sleep(3)

def prepare_insert_query(q, producer, stat_producer_q, printer=None, topic=None):
    global prepare_insert_query_counter,read_from_middle_counter
    try:
        if producer:
            print("We have a producer queue\n")
        if printer:
            printer.put("prepare_insert_query printer queue exists\n")
        #current_ru_maxrss = 0
        sample_memory_usage('prepare_insert_query')
        if not q:
            oops = "There is no events Queue, Exiting"
            print(oops)
            syslog.syslog(syslog.LOG_CRIT, oops)
            safe_exit()
        if not producer:
            oops = "There is no producer queue, Exiting"
            print(oops)
            syslog.syslog(syslog.LOG_CRIT, oops)
            safe_exit()

        print ("topic: {}\n".format(topic))
        if producer:
            if(topic and 1 < len(topic.split(","))):
                topics=topic.split(",")
                if printer: printer.put("topics: {}\n".format(topics))
            else:
                topics=[topic,]
        event_processor=Xcast_event_table()
        ignored_events = []
        ignored_topics = []
        while producer:
            if time_to_go():
                break
            try:
                sample_memory_usage('prepare_insert_query')
                if event_processor:
                    pass
                else:
                    event_processor=Xcast_event_table()
                record=q.get()
                if(record):
                    ev_type=record["Event"]
                    if 'STAT' == ev_type:
                        read_from_middle_counter -= 1       # not propagating this one, so reseting counter
                        q.task_done()
                        #fields= json.dumps(record, separators=(',',':'), sort_keys=True)
                        stat_producer_q.put((ev_type, record))
                        continue
                    #print(ev_type) #DEBUG
                    #if printer: printer.put(record)

                    if event_processor:
                        #resources.append(event_processor)
                        table_name= event_processor.get_table_name(ev_type)
                        if not table_name:
                            q.task_done()
                            read_from_middle_counter -= 1       # not propagating this one, so reseting counter
                            if ev_type not in ignored_events:
                                ignored_events.append(ev_type)
                                syslog.syslog(syslog.LOG_CRIT, "Unknown Event ignored '{}'\n".format(ev_type))
                                syslog.syslog(syslog.LOG_INFO, "echo '{}' | python -m json.tool\n".format(json.dumps(record, sort_keys=True, separators=(",",":"))))
                            continue
                        #print(table_name) #DEBUG
                        read_topic = 'middle_'+table_name

                        #fields= "\t".join(table_values)+"\n"                OLD TSV, before https://jira.xcastlabs.net/browse/MON-6

                        #syslog.syslog(syslog.LOG_ERR, "prepare_insert_query: table: {}\n".format(read_topic))
                        if(topics and read_topic not in topics):
                            q.task_done()
                            read_from_middle_counter -= 1
                            if read_topic not in ignored_topics:
                                ignored_topics.append(read_topic)
                                syslog.syslog(syslog.LOG_CRIT, "Unknown topic ignored '{}'\n".format(read_topic))
                                syslog.syslog(syslog.LOG_CRIT, "echo '{}' | python -m json.tool\n".format(json.dumps(record, sort_keys=True, separators=(",",":"))))
                            continue
                        else:
                            record_values={}
                            json_table_values = {}
                            for k in record:
                                if 'dos' == table_name and 'Shield' == k:
                                    record[k] = ('0','1')[record[k] == 'On']
                                record_values.update({k: record[k]})
                            counter=0
                            for k in record_values:#sorted(Xcast_event_table.middle_events_field_names[table_name]):
                                #print(table_name,k)
                                value = record_values[k]
                                #print(table_name, k, value)
                                QuickK = event_processor.rename_field(table_name, k)
                                #print(QuickK, value)
                                json_table_values.update({QuickK: value})
                                #print(counter,table_values[counter])
                                counter += 1
                            try:
                                if producer:
                                    fields= json.dumps(json_table_values)
                                    producer.put((read_topic, fields))
                                    prepare_insert_query_counter += 1
                                    #printer.put("prepare_insert_query: sent\n")
                                q.task_done()
                            except Exception as inst:
                                messages = ["prepare_insert_query", "Submit fields to producer Queue Oops",
                                            "{}".format(type(inst)), "{}".format(inst.args), "{}".format(inst), "{} {}".format(__file__, 'prepare_insert_query Exiting')]
                                for i in range(len(messages)):
                                    oops = messages[i]
                                    print(oops)
                                    syslog.syslog(syslog.LOG_CRIT, oops)
                                safe_exit()
                    else:
                        syslog.syslog(syslog.LOG_ERR, "could not create Xcast_event_table Object\n")
                else:
                    syslog.syslog(syslog.LOG_DEBUG, "there are no records")
            except Exception as inst:
                messages = ["Exception", "{}".format(type(inst)), "{}".format(inst.args), "{}".format(inst), "{} {}".format(__file__, 'prepare_insert_query Reading producer Queue Oops')]
                for i in range(len(messages)):
                    oops = messages[i]
                    print(oops)
                    syslog.syslog(syslog.LOG_CRIT, oops)
                safe_exit()
        safe_exit()
    except Exception as inst:
        messages = ["Exception", "{}".format(type(inst)), "{}".format(inst.args), "{}".format(inst), "{} {}".format(__file__, 'prepare_insert_query main Oops')]
        for i in range(len(messages)):
            oops = messages[i]
            print(oops)
            syslog.syslog(syslog.LOG_CRIT, oops)
        safe_exit()
    safe_exit()

def read_from_middle(sock, events_q):
    global read_from_middle_counter
    #current_ru_maxrss = 0
    use_python2 = sys.version_info < (3, 0)
    try:
        while True:
            if time_to_go():
                break
            sample_memory_usage('read_from_middle')
            if use_python2:
                data, addr = sock.recvfrom(MAX_SIZE)
            else:
                bdata, addr = sock.recvfrom(MAX_SIZE)
                data=bdata.decode()
            if(data):
                #print(data)
                read_from_middle_counter += 1
                #safe_exit()
                pos = data.find("Self:")
                #print(data, pos)
                when=time.time()
                data += "event_timestamp: {:18.9f}\n".format(when)
                if 0 > pos:
                    data += "Self: {}\n".format(addr[0]) # change of name to be compatible with older middle
                #bdata =data.encode('utf-8')
                #print(data)
                #safe_exit()
                #print("read_from_middle listening, counter = {}".format(read_from_middle_counter))
                to_db(data,events_q)
    except Exception as inst:
        messages = ["Exception", "{}".format(type(inst)), "{}".format(inst.args), "{}".format(inst), "{} {}".format(__file__, 'prepare_insert_query main Exiting')]
        for i in range(len(messages)):
            oops = messages[i]
            print(oops)
            syslog.syslog(syslog.LOG_CRIT, oops)
        safe_exit()
    safe_exit()

def ponger(port):
    try:
        sock = socket(AF_INET,SOCK_DGRAM)
        sock.bind(('0.0.0.0',port))
        message='pong'
        counter=0
        #print ("port={}".format(port))
        while True:
            if time_to_go():
                break
            data, addr = sock.recvfrom(MAX_SIZE)
            #print(data, addr)
            if(data):
                if data.lower() == 'ping':
                    sock.sendto(message.encode('utf-8'),addr)
            else:
                time.sleep(0.1)
                #print("ponger is waiting... {}".format(counter))
                counter += 1
            '''    DEBUG
            counter += 1
            if 50 < counter:
                break
            '''
        safe_exit()
    except Exception as inst:
        messages = ["Exception", "{}".format(type(inst)), "{}".format(inst.args), "{}".format(inst), "{} {}".format(__file__, 'ponger Oops','Exiting')]
        for i in range(len(messages)):
            oops = messages[i]
            print(oops)
            syslog.syslog(syslog.LOG_CRIT, oops)
        safe_exit()

def collect_middle_events(producer, producer_q, topic, port, printer):
    try:
        sock = socket(AF_INET,SOCK_DGRAM)
        sock.bind(('0.0.0.0',port))
        if (sys.version_info < (3, 0)):
            events_q = Queue(maxsize=0)
        else:
            events_q = queue.Queue(maxsize=0)
        for i in range(1):
            worker = Thread(target=prepare_insert_query, args=(events_q, producer, producer_q, printer, topic))
            worker.setDaemon(True)
            resources.append(worker)
            worker.start()
        for i in range(1):
            middle_worker = Thread(target=read_from_middle, args=(sock,events_q))
            middle_worker.setDaemon(True)
            resources.append(middle_worker)
            middle_worker.start()

        while True:
            if time_to_go():
                break
            if producer:
                time.sleep(0.001)
            else:
                break
    except Exception as inst:
        messages = ["Exception", "{}".format(type(inst)), "{}".format(inst.args), "{}".format(inst), "{} {}".format(__file__, 'collect_middle_events Oops', 'Exiting')]
        for i in range(len(messages)):
            oops = messages[i]
            print(oops)
            syslog.syslog(syslog.LOG_CRIT, oops)
        safe_exit()
    safe_exit()

def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert middle events stream into kafka producer')
    parser.add_argument('--config', '-c', type=str, required=False, default = '/usr/local/registrator/cfg/middle_producer_setup.cfg',
                        help='path to config file')
    parser.add_argument('--version', '-v', required=False, action="store_true",
                        help='Prints software version signatures')
    return parser.parse_args()

def time_to_go():
    global max_resources_size
    resources_size = len(resources)
    if resources_size < max_resources_size:
        messages = ["time_to_go:", "Current resources_size  < Max resources_size: {} < {}".format(resources_size, max_resources_size)]
        for i in range(len(messages)):
            oops = messages[i]
            print(oops)
            syslog.syslog(syslog.LOG_CRIT, oops)
        return True
    elif max_resources_size < resources_size:
        max_resources_size = resources_size
    return False

if __name__ == '__main__':
    version_statement="\tProducer:\n{:->45}\n\tLibrary:\n{:->45}".format(DATE, middle_event_structure_DATE)
    args = parse_args()
    if args.version:
        print (version_statement)
        exit(0)
    config_file_path = args.config
    print("--config={}".format(args.config))
    if os.path.isfile(config_file_path):
        config_file = config_file_path
    else:
        print("Can't file the config file with --config={}".format(config_file))
        config_file = "/usr/local/registrator/cfg/{}".format(config_file_path)
    file_config = configparser.SafeConfigParser()
    if not os.path.isfile(config_file):
        print("Can't file the config file with --config={}".format(config_file))
        exit(-1)
    file_config.read([config_file])
    print("Using {} as config".format(os.path.abspath(config_file)))
    #log.configure(file_config.get('log', 'level'))
    listen_to_port=int(file_config.get('producer', 'listen_to_port'))
    pong_to_port=int(file_config.get('producer', 'pong_to_port'))
    if pong_to_port == listen_to_port:
        print ("Please use different ports for pong and listen_to_middle")
        safe_exit()
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
    use_syslog_cfg_value=file_config.get('log', 'syslog')
    use_syslog = [use_syslog_cfg_value.lower() == 'true'][0]
    print(use_syslog_cfg_value, use_syslog)
    if use_syslog:
        print_level = syslog_priorities[file_config.get('log', 'level')]
        facility_cfg_value = file_config.get('log', 'facility')
        print("facility_cfg_value ='{}' '{}'\n".format(facility_cfg_value, 0 < len(facility_cfg_value)))
        if 0 < len(facility_cfg_value):
            facility = int(facility_cfg_value)
        else:
            facility = 17
        print(facility_cfg_value, print_level, facility)
        mask = syslog.LOG_UPTO(print_level)
        syslog.openlog(logoption=syslog.LOG_PID, facility=facility)
        old_mask = syslog.setlogmask(mask)
        messages = version_statement.replace('\t','').split('\n')
        for i in range(len(messages)):
            oops = messages[i]
            #print(oops)
            syslog.syslog(syslog.LOG_ERR, oops)
    try:
        send_to_address = file_config.get('stats', 'send_to_address')
        send_to_port = int(file_config.get('stats', 'send_to_port'))
    except:
        pass
    if not send_to_address or not send_to_port:
        send_to_address =   'logserver3-la.siptalk.com'
        send_to_port    =   3666
        syslog.syslog(syslog.LOG_ERR, 'Please set stats section in config file')
        syslog.syslog(syslog.LOG_ERR, "Using send_to_address = '{}, send_to_port = {}".format(send_to_address, send_to_port))
    printer_q = None

    if (sys.version_info < (3, 0)):
        printer_q = Queue(maxsize=0)
    else:
        printer_q = queue.Queue(maxsize=0)
        print("use_syslog = {}, print_level = {}".format(use_syslog, print_level))
        if printer_q:
            if use_syslog:
                for i in range(1):
                    worker = Thread(target=my_syslog_printer, args=(printer_q,))
                    worker.setDaemon(True)
                    resources.append(worker)
                    worker.start()
            else:
                for i in range(1):
                    worker = Thread(target=my_std_printer, args=(printer_q,))
                    worker.setDaemon(True)
                    resources.append(worker)
                    worker.start()

    print("topics: {}\n".format(topics))
    #print("NOT ready to produce topic {}\n".format(topic))
    try:
        producer = KafkaProducer(client_id=client_id, compression_type=compression, bootstrap_servers=bootstrap_servers, security_protocol=security_protocol, sasl_mechanism=sasl_mechanism, sasl_plain_username=user,sasl_plain_password=password)
    except Exception as inst:
        messages = ["Exception: Can't Start producer", "{}".format(type(inst)), "{}".format(inst.args), "{}".format(inst), "{} {}".format(__file__, 'creating producer Oops')]
        for i in range(len(messages)):
            oops = messages[i]
            print(oops)
            syslog.syslog(syslog.LOG_ERR, oops)
        safe_exit()

    print("Producer was created")
    if producer:
        resources.append(producer)
        #print("ready to produce topic {}\n".format(topic))
        if('middle_dos' == testing_topic):
            dummy_dos(producer,testing_topic)
            producer.close()
            safe_exit()
        if('middle_active' == testing_topic):
            dummy_active(producer,testing_topic)
            producer.close()
            safe_exit()
        if (sys.version_info < (3, 0)):
            producer_q = Queue(maxsize=0)
            stat_producer_q = Queue(maxsize=0)
        else:
            producer_q = queue.Queue(maxsize=0)
            stat_producer_q = queue.Queue(maxsize=0)
        metricsServer = {'address' : send_to_address, 'port': send_to_port}
        stat_producer_thread = Thread(target=my_stat_producer, args=(metricsServer, stat_producer_q, printer_q))
        stat_producer_thread.setDaemon(True)
        resources.append(stat_producer_thread)
        stat_producer_thread.start()

        producer_thread = Thread(target=my_producer, args=(producer, producer_q, printer_q))
        producer_thread.setDaemon(True)
        resources.append(producer_thread)
        producer_thread.start()
        try:
            for i in range(1):
                worker = Thread(target=ponger, args=(int(pong_to_port),))
                worker.setDaemon(True)
                resources.append(worker)
                worker.start()
            for i in range(1):
                worker = Thread(target=collect_middle_events, args=(producer_q, stat_producer_q, topics, int(listen_to_port), printer_q))
                worker.setDaemon(True)
                resources.append(worker)
                worker.start()
        except Exception as inst:
            print (type(inst))
            print (inst.args)
            print (inst)
            print (__file__, 'creating workers Oops')
            safe_exit()
        try:
            reporter = PeriodicReporter('Periodic Changes')
            counter = 0
            sample_memory_usage('main loop')
            reporter.report()
            print('main loop ' + periodic_print_template.format(ru_maxrss, read_from_middle_counter, prepare_insert_query_counter, producer_counter, len(resources)))
            if use_syslog:
                syslog.syslog(syslog.LOG_ERR, 'main loop ' + periodic_print_template.format(ru_maxrss, read_from_middle_counter, prepare_insert_query_counter, producer_counter, len(resources)))
            seconds_until_next_minute = 60 - (int(time.time()) % 60)
            while len(resources) > 0:
                if time_to_go():
                    break
                sample_memory_usage('main loop')
                if counter >= seconds_until_next_minute:
                    seconds_until_next_minute = 60 - (int(time.time()) % 60)

                    ''''
                        if use_syslog:
                            syslog.syslog(syslog.LOG_ERR, 'main loop ' + periodic_print_template.format(ru_maxrss, read_from_middle_counter, prepare_insert_query_counter, producer_counter, len(resources)))
                        else:
                            print('main loop ' + periodic_print_template.format(ru_maxrss, read_from_middle_counter, prepare_insert_query_counter, producer_counter, len(resources)))
                    '''
                    reporter.report()
                    counter = 0
                time.sleep(1)
                counter += 1
        except Exception as inst:
            print (type(inst))
            print (inst.args)
            print (inst)
            print (__file__, 'main loop Oops')
            safe_exit()
    else:
        oops = "Can't Start producer. Exiting"
        print(oops)
        syslog.syslog(syslog.LOG_ERR, oops)
    if use_syslog:
        syslog.closelog()
    safe_exit()
