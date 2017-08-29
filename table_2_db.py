#!/usr/bin/env python

import argparse, sys
import pandas as pd

from influxdb import DataFrameClient
from nested_print import dump, dumpclean
from time import sleep

retention_policy = 'awesome_policy'

def main(host='localhost', port=8086, chunk=100):
    user = 'root'
    password = 'root'
    dbname = 'logs'
    first = True
    chunk_size = chunk

    client = DataFrameClient(host, port, user, password, dbname)
    done = False
    while not done:
        try:
            if first:
                df = pd.read_table(sys.stdin, parse_dates=True,index_col=[1],header=0,nrows=chunk_size,engine='python')
                #df = pd.read_table(sys.stdin, parse_dates=True,index_col=[1],header=0,nrows=chunk_size,engine='c')
                if df.empty:
                    done = True
                    print "Done!"
                    break
                else:
                    #names = df.axes[1][1:]
                    names = df.axes[1]
                    measurement = "{}.{}".format(dbname, df.iloc[0][0])
                    print "Create database: {}.{}, measurement={}".format(retention_policy, dbname, measurement)
                    client.create_database(dbname)
                    client.create_retention_policy(retention_policy, '3d', 3, default=True)
                    print("Create pandas DataFrame. chunk_size={}, names={}".format(chunk_size, names))
                    first = False
            else:
                print("continue using pandas DataFrame. chunk_size={}, names={}".format(chunk_size, names))
                df =pd.read_table(sys.stdin, parse_dates=True,index_col=[1],nrows=chunk_size,names=names,engine='python')
                #df =pd.read_table(sys.stdin, parse_dates=True,index_col=[1],nrows=chunk_size,names=names,engine='c')
            if df.empty:
                done = True
                print "Done!"
                break
            else:
                #dump(df)
                sleep(chunk_size/1000)
                try:
                    client.write_points(df,measurement,tag_columns=[2,3],field_columns=range(3,len(df.axes[1])))
                except Exception as inst:
                    dump(df)
                    print type(inst)
                    print inst.args
                    print inst
                    print __file__, 'Oops'
                    break
        #except IndexError:continue
        #except ValueError:continue
        except Exception as inst:
            dump(df)
            print type(inst)
            print inst.args
            print inst
            print __file__, 'Oops'
            pass
    if(not df.empty):
        try:
            client.write_points(df,measurement,tag_columns=[2,3],field_columns=range(3,len(df.axes[1])))
        except:pass

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
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        print __file__, 'Oops'
