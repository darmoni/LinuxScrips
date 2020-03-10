ID='$Id$'.replace(' $','').replace('$','')
DATE='$Date$'.replace(' $','').replace('$','')

#File name "middle_event_structure.py"

import re
def separate_addr_port(key, value,fields):
    #print("separate_addr_port({},{},{}".format(key, value,fields))
    if(key in Xcast_event_table.fields_with_ports):
        with_port = Xcast_event_table.fields_with_ports[key]
    #if(key.lower() in Xcast_event_table.fields_with_ports):
        m=re.match(r"(.+):(\d+)$",value)
        if m:
            fields[with_port[0]]=m.group(1).strip()
            fields[with_port[1]]=m.group(2).strip()
            return True
    else:
        #fields[key.strip()] = value.strip()
        return False

def translate_field(x,v):
    return {
        'int': int(float(v)),
        'float64': float(v),
    }.get(x.lower(), v)

'''
[mevent] 07:55:39.358774 Event: INVITE
UniqNo: 67101
Domain: siptalk64.xcastlabs.com
Direction: CLN
From: 27065
To: 00
'''

'''
Event: STAT
MaxQueueSize: 3,4
ExtProc: 17,1
IntProc: 19,1
Method: SUBSCRIBE:6,NOTIFY:12
Bounce: 404:21,408:5,500:4
BadEvent: as-feature-event:1,line-seize:9
Dos: L:2,H:4
Self: 75.145.154.234:7060
'''
middle_events_field_names={
    "test":         ['Event','event_timestamp','Self','Testing','Tested'],
    "dos":          ['Event','event_timestamp','Self','IP','Port','Shield'],
    "call":         ['Event','event_timestamp','Self','UniqNo','Domain','Direction','From','from_port','To','to_port','Extra','FMode'],
    "registration": ['Event','event_timestamp','Self','Domain','CallID','IntIP','private_port','Agent','AOR','Line','ExtIP','public_port','Reason'],
    "active":       ['Event','event_timestamp','Self','Full','Dialogs','Calls','Extra','Started','Regs']
    , "stats":        ['Event','event_timestamp','Self','MaxQueueSize','ExtProc','IntProc']
    }
tables={
    "test":         ['event','event_timestamp','sbc_ip','testing','tested'],
    "dos":          ['event','event_timestamp','sbc_ip','ip','port','blocked'],
    "call":         ['event','event_timestamp','sbc_ip','uniq_id','domain','direction','from','from_port','to','to_port','extra','full_mode_type'],
    "registration": ['event','event_timestamp','sbc_ip','domain','call_id','private_ip','private_port','agent','aor','line','public_ip','public_port','reason'],
    "active":       ['event','event_timestamp','sbc_ip','full_mode','dialogs','calls','extra','started_timestamp','registrations']
    , "stats":        ['event','event_timestamp','sbc_ip','max_queue_size','ext_proc','int_proc']
    }

class middle_events_table:
    def __init__(self, middle_2_clickhouse_field_names):
        self.field_names = middle_2_clickhouse_field_names


    def get_clickhouse_name(self,table_name, middle_field_name):
        if middle_field_name in self.field_names[table_name].keys():
            return self.field_names[table_name][middle_field_name]

class Xcast_event_table:

    xcast_event_tables={}
    non_string_fields={'event_timestamp':'Float64', 'Blocked':'int', 'Blocked'.lower():'int', 'started_timestamp'.lower():'UInt64', 'public_port':'UInt16', 'private_port':'UInt16'}
    fields_with_ports={'From':['From','from_port'], 'To':['To','to_port'], 'ExtIP':['ExtIP','public_port'] ,'IntIP':['IntIP','private_port']}
    table_names_dict={
    "test":['testing',],
    "dos":['block', 'unblock', 'ddos'],
    "registration":['reg','unreg','faild'],
    "call":['invite','timeout','bye','cancel','talk', 'dtor','reject','srv_audio','cln_audio','srv_video','cln_video'],
    "active": ['active','stop']
    #, "stats": ['stat',]
    }

    def get_table_name(self, ev_type):
        for key in Xcast_event_table.table_names_dict:
            if ev_type.lower() in Xcast_event_table.table_names_dict[key]:
                table_name = key
                #print "table_name = %s " % table_name
                return table_name

    def rename_field(self, table, middle_field):      # normalize middle Field name into ClickHouse monitor table field names
        return self.xlator.get_clickhouse_name(table, middle_field)

    def __init__(self):

        field_maps={}
        for table_name in middle_events_field_names.keys():
            table_field_map={}
            for middle_field in middle_events_field_names[table_name]:
                field_index = middle_events_field_names[table_name].index(middle_field)
                pair={middle_field:tables[table_name][field_index]}
                table_field_map.update(pair)
            field_maps.update({table_name:table_field_map})

        self.xlator = middle_events_table(field_maps)

    def __del__ (self):
        #del Xcast_event_table.xcast_event_tables
        pass
