#!/usr/bin/env python

from socket import socket, AF_INET, SOCK_DGRAM
from influxdb import InfluxDBClient
from influxdb import SeriesHelper
import argparse
#from nested_print import dump, dumpclean
import time
import shlex, sys, signal
from subprocess import Popen, PIPE
if sys.version_info < (3,0,0):
    from nbstreamreader import NonBlockingStreamReader as NBSR

retention_policy = 'awesome_policy'


global test_server

def safe_exit(level):
    global test_server
    print 'Killing Server'
    test_server.stdin.write("q\n")
    time.sleep(0.1)
    test_server.kill()
    exit(0)

def sig_handler(sig, frame):
    print "got sig(", sig,")\n"
    safe_exit(sig)

signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)

class unregistering_event:
    def __init__(self, single, measurement):
        self.measurement=measurement
        #print("unregistering_event: ",single)
        fields={}
        #lines = single.strip().replace("\\n","\n").split("\n")
        lines = single.replace("\\n","\n").split("\n")

        #print ("unregistering_event: ",lines)
        #return
        try:
            self.ev_ready = False
            self.ev_started = False
            self.index_of_type=0
            for line in range(len(lines)):
                l=lines[line]
                #print (l,lines[line])
                if (2 > l.find(":")) : continue
                parts = l.split()
                key=parts[0].strip()
                value=parts[1].strip()
                #print(key,value)
                if(False == self.ev_started and ("Event:" == key)):
                    if ("UNREG" != value) : return
                    self.index_of_type = line
                    self.ev_started = True
                fields[key]=value
            if((False == self.ev_started) or (4 > (len(fields) - self.index_of_type))): # 0 based list
                self.ev_ready = False
                print (len(fields), self.index_of_type)
                return None
            #print ("unregistering_event: ", len(fields), self.index_of_type)
            #return None
            self.ev_type = fields["Event:"]
            self.ev_domain = fields["Domain:"]
            self.ev_line = fields["Line:"]
            self.ev_aor = fields["AOR:"]
            self.time = int(time.time() * 1000000000)
            self.ev_ready = True
            self.point = {
                    "measurement": measurement,
                    "time":   self.time,
                    "fields": {
                        "aor":          self.ev_aor,
                    },
                    "tags": {
                        "type":         self.ev_type,
                        "domain":       self.ev_domain,
                        "line" :        self.ev_line,
                    }
                }
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print(__file__, 'Oops')
            if(self.point):
                print (self.point)
            self.ev_ready = False

    def tostring(self):
                command = "insert into {} time={}, AOR='{}', type='{}, 'domain='{}', line='{}'". \
                    format(self.measurement, self.time, self.ev_aor, self.ev_type,self.ev_domain,self.ev_line)
                return command

class registering_event:
    def __init__(self, single, measurement):
        self.measurement=measurement
        #print("registering_event: ",single)
        fields={}
        lines = single.replace("\\n","\n").split("\n")
        try:
            self.ev_ready = False
            self.ev_started = False
            self.index_of_type=0
            for line in range(len(lines)):
                l=lines[line]
                if (2 > l.find(":")) : continue
                parts = l.split()
                key=parts[0].strip()
                value=parts[1].strip()
                #print(key,value)
                if(False == self.ev_started and ("Event:" == key)):
                    if ("REG" != value) : return
                    self.index_of_type = line
                    self.ev_started = True
                fields[key]=value
                #print(key,value)

            if((False == self.ev_started) or (8 > (len(fields) - self.index_of_type))): # 0 based list
                self.ev_ready = False
                print (len(fields), self.index_of_type)
                return None
            self.ev_type = fields["Event:"]
            self.ev_call_id = fields["CallID:"]
            self.ev_domain = fields["Domain:"]
            self.ev_line = fields["Line:"]
            self.ev_internal_ip = fields["IntIP:"]
            self.ext_ip = fields["ExtIP:"]
            self.ev_agent = fields["Agent:"]
            self.ev_aor = fields["AOR:"]
            self.time = int(time.time() * 1000000000)
            self.ev_ready = True
            self.point = {
                    "measurement": measurement,
                    "time":   self.time,
                    "fields": {
                        "aor":          self.ev_aor,
                        "call_id":      self.ev_call_id,
                        "agent":        self.ev_agent,
                        "internal_ip":  self.ev_internal_ip,
                        "ext_ip":         self.ext_ip,
                    },
                    "tags": {
                        "type":         self.ev_type,
                        "domain":       self.ev_domain,
                        "line" :        self.ev_line,
                    }
                }
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print(__file__, 'Oops')
            if(self.point):
                print (self.point)
            self.ev_ready = False

    def tostring(self):
                command = "insert into {} time={}, AOR='{}', type='{}', call_id='{}', domain='{}', line='{}', internal_ip='{}', ext_ip='{}', agent='{}'". \
                    format(self.measurement, self.time, self.ev_aor, self.ev_type,self.ev_call_id,self.ev_domain,self.ev_line,self.ev_internal_ip,self.ext_ip,self.ev_agent)
                return command

def process_event(event, measurement):
    print("process_event: " + event)
    type_pos=event.find(b'Event: ')
    #print("process_event: ", event)
    if(0 <= type_pos):
        reg_pos = event[type_pos:].find(b'REG')
        unreg_pos = event[type_pos:].find(b'UNREG')
        if(0 <= unreg_pos):
            #print ("unreg_pos = {}".format(unreg_pos))
            db_insert = unregistering_event(event[type_pos:].strip(), measurement)#+".unreg")
        elif (0 <= reg_pos):
            #print ("reg_pos = {}".format(reg_pos))
            db_insert = registering_event(event[type_pos:].strip(), measurement)#+".reg")
        if (db_insert.ev_ready):
            cmd = 'influx -database "reg_events" -precision "ns" -execute "' + db_insert.tostring().format("registration_event") + '"'
            #print (cmd)
            #print(db_insert.point)
            return db_insert.point
        else:
            return None

def events_client(client, nbsr, chunk = 5, measurement="registration_events"):
    try:
        #print("events_client:")
        points = []
        counter = 0
        while True:
            data=nbsr.readline()
            if((None == data) or (0 == len(data))):
                print("events_client: no data yet, counter = {}".format(counter))
                time.sleep(3)
                continue
            #print("events_client: data = ", data)
            point=process_event(data, measurement)
            if((point is None) or (0 == len(point))): continue
            counter += 1
            points.append(point)
            #print ("events_client: point : ", point['tags']['type'])
            if (chunk == counter % (chunk+1)):
               client.write_points(points)
               points = []
               time.sleep(0.3)
            # Write points
        #print("number of points: ", len(points))
        #print(points)
        if(len(points) > 0):
            client.write_points(points)
        points = []

    except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print(__file__, 'Oops')
            #raise SystemExit

def main(host='localhost', port=8086, chunk=100, retention_policy = 'awesome_policy'):
    global test_server
    while True:
        try:
            user = 'root'
            password = 'root'
            dbname = 'reg_events'
            first = True
            chunk_size = chunk
            client = InfluxDBClient(host, port, user, password, dbname)
            #time.sleep(2)
            print("Create database: " + dbname)
            client.create_database(dbname)
            client.switch_database(dbname)
            client.create_retention_policy(retention_policy, '3d', 3, default=True)

            #setup the listener
            args = shlex.split('/home/nir/bin/reg_event_listener.py')
            p = Popen(args, stdin=PIPE, stdout=PIPE,stderr=PIPE, shell=False)
            # wrap p.stdout with a NonBlockingStreamReader object:
            if( p ):
                test_server=p
                nbsr = NBSR(p.stdout)
                print("main: calling events_client")
                events_client(client,nbsr, chunk)
                #while True:
                #    print(p.stdout.read())
        except Exception as inst:
                #(type(inst))
                p.kill()
                print(inst.args)
                print(inst)
                print(__file__, 'Oops')
                #raise SystemExit

    p.kill()

def parse_args():
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    parser.add_argument('--chunk', type=int, required=False, default=100,
                        help='Size of data chunk to use')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    #dump(args)
    try:
        main(host=args.host, port=args.port, chunk=args.chunk)
    except:
        exit (-1)
