#!/usr/bin/env python

import argparse, sys
import pandas as pd

from influxdb import DataFrameClient


def main(host='localhost', port=8086):
    user = 'root'
    password = 'root'
    dbname = 'logs'
    measurement ='conf'
    # Temporarily used to avoid line protocol time conversion issues #412, #426, #431.
    #protocol = 'json'

    try:
        client = DataFrameClient(host, port, user, password, dbname)
        print("Create database: " + dbname)
        client.create_database(dbname)
        print("Create pandas DataFrame")
        df = pd.read_table(sys.stdin, parse_dates=True,index_col=[2],header=0)
        #df = pd.read_table(sys.stdin, parse_dates=True,index_col=[2],header=0),nrows=20,engine='python')
        '''
        names = df.axes[1]
        while True:
            print "reading 10 lines"
            more =pd.read_table(sys.stdin, parse_dates=True,nrows=10,names=names,engine='python')
            if more.empty:
                print "Done!"
                break
            else:
                df.append(more)
                print "Got more?"
        '''
        #df = pd.DataFrame(data=list(range(30)),
        #                  index=pd.date_range(start='2017-05-05',
        #                                      periods=30, freq='S'))
        #o = df.to_json( orient='index')
        #print ("Dataframe as Json '{}\n'".format(o))
        print("Write DataFrame")
        client.write_points(df, measurement,tag_columns=[2,3],field_columns=[4])
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        print __file__, 'Oops'
    #client.write_points(o, measurement, protocol=protocol,tag_columns=[3,4],field_columns=5)

    #print("Write DataFrame with Tags")
    #client.write_points(df, 'demo', {'k1': 'v1', 'k2': 'v2'}, protocol=protocol)

    #print("Read DataFrame")
    #client.query("select * from %s" % measurement)

    #print("Delete database: " + dbname)
    #client.drop_database(dbname)


def parse_args():
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)
