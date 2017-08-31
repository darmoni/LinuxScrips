#!/usr/bin/env python
# $Id$ $Date$
import argparse, sys
import pandas as pd
from time import sleep

from influxdb import InfluxDBClient, DataFrameClient
from influxdb import SeriesHelper
from nested_print import dump, dumpclean,deepdive

retention_policy = 'awesome_policy'

def main(server_name='', test_mode='', host='localhost', port=8086, chunk=100):
    user = 'root'
    password = 'root'
    dbname = 'MediaPerfomance'
    first = True
    chunk_size = chunk

    client = DataFrameClient(host, port, user, password, dbname)
    client.create_database(dbname)
    client.create_retention_policy(retention_policy, '3d', 3, default=True)
    done = False
    while not done:
        try:
            if first:
                print("Create pandas DataFrame")
                df = pd.read_table(sys.stdin, parse_dates=True,index_col=[1],header=0,nrows=chunk_size,engine='python')
                if df.empty:
                    done = True
                    print "Done!"
                    break
                else:
                    names = df.axes[1][1:]
                    if('' != test_mode): measurement = "{}.{}.{}".format(df.iloc[0][0],server_name,test_mode)
                    else: measurement = "{}.{}".format(df.iloc[0][0],server_name)
                    print "Create database: {}, measurement={}".format(dbname, measurement)
                    first = False
            else:
                df =pd.read_table(sys.stdin, parse_dates=True,index_col=[1],nrows=chunk_size,names=names,engine='python')
            if df.empty:
                done = True
                print "Done!"
                break
            else:
                #dump(df)
                print("range = {}".format(len(df.axes[1])))
                #dump(df.axes)
            sleep(2)
            client.write_points(df,measurement,tag_columns=[1,2],field_columns=range(2,len(df.axes[1])))
        except ValueError:continue
        except Exception as inst:
            print type(inst)
            print inst.args
            print inst
            print __file__, 'Oops'
            break
    if(not df.empty):
        #dump(df)
        try:
            client.write_points(df,measurement,tag_columns=[1,2],field_columns=range(2,len(df.axes[1])))
        except:pass

def parse_args():
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    parser.add_argument('--chunk', type=int, required=False, default=1000,
                        help='Size of data chunk to use')
    parser.add_argument('--test_server', type=str, required=False,
                        default='staging',
                        help='PBX System alias')
    parser.add_argument('--test_mode', type=str, required=False,
                        default='vad_on',
                        help='Test Mode')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    #dump(args)
    try:
        main(server_name=args.test_server, host=args.host, port=args.port, chunk=args.chunk, test_mode=args.test_mode)
    except Exception as inst:
        print (type(inst))
        print (inst.args)
        print (inst)
        print (__file__, 'Oops')
