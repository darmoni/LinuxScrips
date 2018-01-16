#!/usr/bin/env python3

"""
Sample
Event: REG
CallID: 1661796768_59574292@4.55.17.227
Domain: xcastlabs.voippbsite.net
Line: 7065D01L01
IntIP: 10.10.8.21
Hole: 75.145.154.225:2048
Agent: Cisco/SPA508G-7.6.2b
Timestamp: 1515794119

"""
from socket import socket, AF_INET, SOCK_DGRAM

from influxdb import InfluxDBClient
from influxdb import SeriesHelper
import argparse
#from nested_print import dump, dumpclean
import time

#retention_policy = 'awesome_policy'

'''
class MySeriesHelper(SeriesHelper):
    # Meta class stores time series helper configuration.
    class Meta:
        # The client should be an instance of InfluxDBClient.
        client = myclient
        # The series name must be a string. Add dependent fields/tags in curly brackets.
        series_name = 'events.regs.{server_name}'
        # Defines all the fields in this time series.
        fields = ['type','call_id','internal_ip','hole','agent','ts']
        # Defines all the tags for the series.
        tags = ['server_name', 'domain','line']
        # Defines the number of data points to store prior to writing on the wire.
        bulk_size = 5
        # autocommit must be set to True when using bulk_size
        autocommit = True
'''
class registering_event:
    def __init__(self, single, measurement):
        #print(single)
        fields={}
        lines = single.decode().strip().replace("\\n","\n").split("\n")
        #lines = single.decode().replace("\\n","\n").split("\n")

        #print ("registering_event: ",lines)
        try:
            self.ev_ready = False
            self.ev_started = False
            self.index_of_type=0
            for line in range(len(lines)):
                l=lines[line]
                #print (l,lines[line])
                if (3 > l.find(":")) : continue
                parts = l.split()
                key=parts[0].strip()
                value=parts[1].strip()
                if(False == self.ev_started and ("Event:" == key)):
                    if (("UNREG" != value) and ("REG" != value)) : return 
                    self.index_of_type = line
                    self.ev_started = True
                if ("Timestamp:" == key):
                    #print (key, int(float(value))) 
                    fields["Timestamp:"]=int(float(value))
                else:
                    fields[key]=value
                #print(key,value)

            if((False == self.ev_started) or (8 < (len(fields) - self.index_of_type))): # 0 based list
                self.ev_ready = False
                #print (len(fields), self.index_of_type)
                return
            self.ev_type = fields["Event:"]
            self.ev_call_id = fields["CallID:"]
            self.ev_domain = fields["Domain:"]
            self.ev_line = fields["Line:"]
            self.ev_internal_ip = fields["IntIP:"]
            self.ev_hole = fields["Hole:"]
            self.ev_agent = fields["Agent:"]
            self.ev_ts = fields["Timestamp:"]
            self.time = int(time.time() * 1000000000)
            self.ev_ready = True
            self.point = {
                    "measurement": measurement,
                    "time":   self.time,
                    "fields": {                        
                        "call_id":      self.ev_call_id,
                    },
                    "tags": {
                        "internal_ip":  self.ev_internal_ip,
                        "hole":         self.ev_hole,
                        "agent":        self.ev_agent,
                        "type":         self.ev_type,
                        "ts":           self.ev_ts,
                        "domain":       self.ev_domain,
                        "line" :        self.ev_line,
                    }
                }
            
            #print (self.point)
            
        except:
            self.ev_ready = False
    
    def tostring(self):
                command = "insert into {} time={}, ts={}, type='{}', call_id='{}', domain='{}', line='{}', internal_ip='{}', hole='{}', agent='{}'". \
                    format("{}", self.time, self.ev_ts, self.ev_type,self.ev_call_id,self.ev_domain,self.ev_line,self.ev_internal_ip,self.ev_hole,self.ev_agent)
                return command
    
def process_event(event, measurement):
    type_pos=event.find(b'Event: ')
    #print("process_event: ", event.decode().strip().replace("\\n","\n").split("\n"))
    if(0 <= type_pos):
        reg_pos = event[type_pos:].find(b'REG')
        unreg_pos = event[type_pos:].find(b'UNREG')
        if ( (0 <= reg_pos) or (0 <= unreg_pos) ):
            db_insert = registering_event(event[type_pos:], measurement)
            #cmd = 'influx -database "my_events" -precision "ns" -execute "' + db_insert.tostring().format("registration_event") + '"'
            #print (cmd)
            return db_insert.point


def events_client(client, measurement="registration_events", host='localhost', port=12345, MAX_SIZE=4096, chunk=10000, PORT= 12345):
    sock = socket(AF_INET,SOCK_DGRAM)
    msg = "Ping"
    points = []
    #print("Client is sending ", msg)
    try:
        for counter in range(10*chunk):
            sock.sendto(msg.encode('utf-8'),('', PORT))
            data, addr = sock.recvfrom(MAX_SIZE)
            #print(data)
            point=process_event(data, measurement)
            if(0 == len(point)): continue
            points.append(point)
            #print ("main: point : ", point)
            if (chunk == counter % (chunk+1)):
               client.write_points(points)
               points = []
               time.sleep(3)
            # Write points
        #print("number of points: ", len(points))
        #print(points)
        client.write_points(points)

    except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print(__file__, 'Oops')
            raise SystemExit

def main(host='localhost', port=8086, chunk=100):
    user = 'root'
    password = 'root'
    dbname = 'reg_events'
    first = True
    chunk_size = chunk

    client = InfluxDBClient(host, port, user, password, dbname)

    print("Create database: " + dbname)
    client.create_database(dbname)
    client.switch_database(dbname)
    #client.create_retention_policy(retention_policy, '3d', 3, default=True)
    events_client(client);


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
