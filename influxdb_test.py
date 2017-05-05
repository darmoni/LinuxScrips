#!/usr/bin/env python

import argparse, shlex, jason
from influxdb import InfluxDBClient
from nested_print import dumpclean,dump,deepdive

measurements_meta = {}

def parse_fields(fields_part, meta):
    #print 'Fields:\n'+ fields_part
    reference_fields = meta.get_fields()
    m = meta.get_measurement()
    #print reference_fields, m
    fields={}
    equal=fields_part.find('=',1)
    name=fields_part[0:equal]
    if( name in reference_fields):
        #print 'Field %s Found in %s' % name, m
        rest = fields_part[equal+1:]
    #print name+'='+'"'+rest+'"'
    #rest = shlex.split(fields[equal+1:])
    #print name+'='+rest[0]
        fields.update({name:rest})
    return fields
'''
class Meta:
        # The client should be an instance of InfluxDBClient.
        client = myclient
        # The series name must be a string. Add dependent fields/tags in curly brackets.
        series_name = 'events.stats.{server_name}'
        # Defines all the fields in this time series.
        fields = ['some_stat', 'other_stat']
        # Defines all the tags for the series.
        tags = ['server_name']
        # Defines the number of data points to store prior to writing on the wire.
        bulk_size = 5
        # autocommit must be set to True when using bulk_size
        autocommit = True

class bad_Meta:
    def __init__(self, m):
        self._f=[]
        self.set_measurement(m)
        
    def set_measurement(self,m):
        self._m = m;
    def get_measurement(self):
        return self._m
    def set_fields(self,f):
        self._f.append(f);
    def get_fields(self):
        return self._f

def line_2_meta(line):

    parts = shlex.split(line)
    #print parts
    
    tags_meas = parts[0].split(',')
    measurement=tags_meas[0]
    return measurement

def line_2_jason(line):

    parts = shlex.split(line)
    #print parts
    
    tags_meas = parts[0].split(',')
    measurement=tags_meas[0]

    number_of_tag = len(tags_meas)-1
    if(0 < number_of_tag):
        tags={}
        for tag in range (1,number_of_tag+1):
            #print 'tag:',tags_meas[tag]
            (name,value) =tags_meas[tag].split('=')
            tags.update({name:value})
    time=parts[-1]
    #print measurement,time
    if(len(parts) > 2):
        fields_area = parts[1]
        fields =parse_fields(fields_area,measurements_meta[measurement])
        #print fields
        json_body = [
            {
                "measurement":measurement,
                "tags": tags,
                "time": time,
                "fields":fields
                }
            ]
        return json_body
'''
def main(host='localhost', port=8086):
    user = 'root'
    password = 'root'
    dbname = 'conferences'
    dbuser = 'smly'
    dbuser_password = 'my_secret_password'
    supported_data_examples= [
     #   'h2o_feet,location=coyote_creek water_level=8.005,level\ description="between 6 and 9 feet" 1439856360'
     #   ,
       'conf,proc=T49f9,subject=HND info="[HND INFO] [ HT_H264_DECODER] total 0, active 0" 09:00:27.936005'
    ]
    client = InfluxDBClient(host, port, user, password, dbname)
    o = [
        {
        "(u'conf', None)": 
            [
                {u'info': u'CloudClient[0xc8f0500] connected, creating MediaCloud', u'subject': u'Master', u'proc': u'13949', u'time': u'2017-05-03T08:23:19.194812928Z'},
                {u'info': u'[HND INFO] [ HT_H264_DECODER] total 0, active 0', u'subject': u'HND', u'proc': u'T49f9', u'time': u'2017-05-03T09:00:27.93600512Z'},
                {u'info': u'[HND INFO] [ HT_H264_DECODER] total 0, active 0', u'subject': u'HND', u'proc': u'T49f9', u'time': u'2017-05-04T09:00:27.93600512Z'}
            ]
        }
    ]
    dump(o)
    #print("Create database: " + dbname)
    #client.create_database(dbname)

    #print("Create a retention policy")
    #client.create_retention_policy('awesome_policy', '3d', 3, default=True)

    #print("Switch user: " + dbuser)
    client.switch_user(dbuser, dbuser_password)
    
    client.write_points(o)
    '''
    for line in supported_data_examples:
        measurement = line_2_meta(line)
        #print 'measurement', measurement
        query = 'select * from %s ' % measurement
        measurements_meta.update({measurement: Meta(measurement)})
        result = client.query('show field keys from "%s"' % measurement)
        fields = list(result)
        fields_collector=[]
        deepdive(fields,'fieldKey',fields_collector)
        for field in fields_collector:
            print field
            measurements_meta[measurement].set_fields(field)
        #print 'Fields:',
    
    dump(measurements_meta[measurement])
    
    for line in supported_data_examples:
        json_body = line_2_jason(line)
        #print("Write points: {0}".format(json_body))

        #print("Result: {0}".format(result))
    
        #print("Write points: {0}".format(json_body))
        #client.write_points(json_body)

        #print("Queying data: " + query)
        result = client.query(query)
        #dump(list(result))

        #print("Result: {0}".format(result))

    client = InfluxDBClient(host, port, user, password, 'NOAA_water_database')
    query = 'SHOW field keys from h2o_feet'
    print("Querying data: " + query)
    result = client.query(query)
    fields = list(result)
    dump(fields)
    fields_collector=[]
    deepdive(fields,'fieldKey',fields_collector)
    print 'Fields:'
    dumpclean(fields_collector)
    print("Result: {0}".format(**fields[0]))

    #print("Switch user: " + user)
    #client.switch_user(user, password)

    #print("Drop database: " + dbname)
    #client.drop_database(dbname)
'''

def parse_args():
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False, default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


if __name__ == '__main__':

    '''
    #dump(o)
    #print 'fields: {info}'.format(**{u'info': u'CloudClient[0xc8f0500] connected, creating MediaCloud', u'subject': u'Master', u'proc': u'13949', u'time': u'2017-05-03T08:23:19.194812928Z'})
    #print 'fields: {info}'.format(**o[0]["(u'conf', None)"][1])
    #coord = {'latitude': '37.24N', 'longitude': '-115.81W'}
    #print 'Coordinates: {latitude}, {longitude}'.format(**coord)
    '''
    args = parse_args()
    main(host=args.host, port=args.port)
