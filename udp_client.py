#!/usr/bin/env python3
from socket import socket, AF_INET, SOCK_DGRAM

MAX_SIZE = 4096
PORT = 12345
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
class registering_event:
    def __init__(self, single):
        #print(single)
        fields={}
        lines = single.decode().strip().replace("\\n","\n").split("\n")
        #lines = single.decode().replace("\\n","\n").split("\n")

        print (lines)
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
                print(key,value)
                if(False == self.ev_started and ("Event:" == key)):
                    if (("REG" != value) and ("UNREG" != value)) : return 
                    self.index_of_type = line
                    self.ev_started = True
                #print(key,value)
                fields[key]=value
            if((False == self.ev_started) or (8 > (1+len(fields) - self.index_of_type))): # 0 based list
                self.ev_ready = False
                print (len(fields), self.index_of_type)
                return
            self.ev_type = fields["Event:"]
            self.ev_call_id = fields["CallID:"]
            self.ev_domain = fields["Domain:"]
            self.ev_line = fields["Line:"]
            self.ev_internal_ip = fields["IntIP:"]
            self.ev_hole = fields["Hole:"]
            self.ev_agent = fields["Agent:"]
            self.ev_ts = fields["Timestamp:"]
            self.ev_ready = True
        except:
            #print(l,fields)
            self.ev_ready = False
    def tostring(self):
        if (self.ev_ready):
            command = "insert into TheTable (type,call_id,domain,line,internal_ip,hole,agent,ts) values ('{}','{}','{}','{}','{}','{}','{}','{}')". \
                format(self.ev_type,self.ev_call_id,self.ev_domain,self.ev_line,self.ev_internal_ip,self.ev_hole,self.ev_agent,self.ev_ts)
            return command
        else:
            return ""
    
def process_event(event):
    print (event)
    type_pos=event.find(b'Event:')
    print("type_pos=",type_pos)
    if(0 <= type_pos):
        db_insert = registering_event(event[type_pos:])
        if (False == db_insert.ev_ready):
            return ""
        else:
            return db_insert.tostring()

if __name__ == '__main__':
    sock = socket(AF_INET,SOCK_DGRAM)
    msg = "Hello UDP server"
    for counter in range(3):
        sock.sendto(msg.encode('utf-8'),('', PORT))
        data, addr = sock.recvfrom(MAX_SIZE)
        #print(data.decode(), "\n")
        print("Server says:{}".format(repr(process_event(data))))
