#!/usr/bin/env python

import argparse
from influxdb import InfluxDBClient

def main(host='localhost', port=8086):
    user = 'root'
    password = 'root'
    dbname = 'conferences'
    dbuser = 'smly'
    dbuser_password = 'my_secret_password'
    query = 'select * from conf;'
    #insert conf,proc=T367d,subject=CLOUD info="[MediaCloud] 0001:HT_CLOUD,0001:HT_WORKTHREAD,0001:HT_AMIXER,0001:HT_VMIXER,src 0001:HT_VCONNECTOR,rnd 0002:HT_VCONNECTOR (1/1+ active)" 1493793068899925
    json_body = [
        {
            "measurement": "conf",
            "tags": {
                "proc": "13949",
                "subject": "Master"
            },
            #"time":          "1493804111899925010",
            #"time": "2017-05-02T23:00:00.899926020Z",
            "time": "08:23:19.194813",
            "fields": {
                "info": "CloudClient[0xc8f0500] connected, creating MediaCloud"
            }
        }
    ]

    client = InfluxDBClient(host, port, user, password, dbname)

    print("Create database: " + dbname)
    client.create_database(dbname)

    print("Create a retention policy")
    client.create_retention_policy('awesome_policy', '3d', 3, default=True)

    print("Switch user: " + dbuser)
    client.switch_user(dbuser, dbuser_password)

    print("Write points: {0}".format(json_body))
    client.write_points(json_body)

    print("Queying data: " + query)
    result = client.query(query)

    print("Result: {0}".format(result))
'''    
    client = InfluxDBClient(host, port, user, password, 'NOAA_water_database')
    query = 'select * from h2o_feet;'
    print("Queying data: " + query)
    result = client.query(query)

    print("Result: {0}".format(result))
'''
    #print("Switch user: " + user)
    #client.switch_user(user, password)

    #print("Drop database: " + dbname)
    #client.drop_database(dbname)


def parse_args():
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False, default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)
