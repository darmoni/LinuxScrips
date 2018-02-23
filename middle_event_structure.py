import re
def separate_addr_port(key, value,fields):
    if(key.lower() in Xcast_event_table.fields_with_ports):
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

class Xcast_event_table:

    xcast_event_tables={}
    non_string_fields={'time':'Float64','Time':'Float64'}
    fields_with_ports=['from','to']
    tables={
        "test":         ['event','time','serverip','testing','tested'],
        "dos":          ['event','time','serverip','ip','port','shield'],
        "call":         ['event','time','serverip','uniqno','domain','direction','from','from_port','to','to_port','extra','fmode'],
        "registration": ['event','time','serverip','domain','callid','intip','agent','aor','line','extip','reason'],
        "active":       ['event','time','serverip','full','dialogs','calls','extra','started','regs']
        }
    table_names_dict={
    "test":['testing',],
    "dos":['block', 'unblock', 'ddos'],
    "registration":['reg','unreg','faild'],
    "call":['invite','timeout','bye','cancel','talk', 'dtor','reject','srv_audio','cln_audio','srv_video','cln_video'],
    "active": ['active','stop']
    }

    def print_table(self,table_name):
        if self.table_name in Xcast_event_table.xcast_event_tables:
            return(self.create_new_table)

    def __init__(self,record,ev_type, table_name_prefix='middle_',keep_old_table=True):
        #print(record,ev_type,table_name_prefix,keep_old_table)
        for key in Xcast_event_table.table_names_dict:
            #print ev_type.lower(), key, Xcast_event_table.table_names_dict[key]
            if ev_type.lower() in Xcast_event_table.table_names_dict[key]:
                table_name = key
                #print "table_name = %s " % table_name
                break
        else: raise SystemExit
        self.table_name=table_name_prefix+table_name
        #print(ev_type,self.table_name,keep_old_table)
        if( self.table_name in Xcast_event_table.xcast_event_tables):
            self.create_new_table=''
            pass
        else:
            drop_old_table="DROP TABLE IF EXISTS {}; ".format(self.table_name)
            other_fields=''
            create_even_if_exists= ('',"IF NOT EXISTS ") [keep_old_table]
            for key in sorted(Xcast_event_table.tables[table_name]):
                if (key in Xcast_event_table.non_string_fields): 
                    type_name=Xcast_event_table.non_string_fields[key]
                else:
                    type_name='String'
                other_fields += (", {} {}".format(key.lower(), type_name))
            self.create_new_table="""{}CREATE TABLE {}{}
(
recdate Date MATERIALIZED toDate(time)
{}
)
ENGINE = MergeTree(recdate, (recdate,serverip), 8192);
""".format((drop_old_table,'')[keep_old_table],create_even_if_exists, self.table_name, other_fields)
            Xcast_event_table.xcast_event_tables.update({self.table_name:self.create_new_table})
    def __del__ (self):
        #del Xcast_event_table.xcast_event_tables
        pass
