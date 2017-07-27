#!/usr/bin/env python

import argparse, sys
import pandas as pd
from time import sleep

from influxdb import InfluxDBClient, DataFrameClient
from influxdb import SeriesHelper
#from nested_print import dump, dumpclean,deepdive

# InfluxDB connections settings
host = 'localhost'
port = 8086
user = 'root'
password = 'root'
dbname = 'MediaPerfomance'
measurement ='ReportPerfomance'


myclient = InfluxDBClient(host, port, user, password, dbname)
myclient.create_database(dbname)
retention_policy = 'awesome_policy'

class MySeriesHelper(SeriesHelper):
    # Meta class stores time series helper configuration.
    class Meta:
        # The client should be an instance of InfluxDBClient.
        client = myclient
        retention_policy = retention_policy
        # The series name must be a string. Add dependent fields/tags in curly brackets.
        series_name = measurement
        # Defines all the fields in this time series.
        fields = ['time','info','queue','rcv','drp','prc','tmr','average_wait','average_run','recent_wait','recent_run']
        # Defines all the tags for the series.
        tags = ['subject','proc']
        # Defines the number of data points to store prior to writing on the wire.
        bulk_size = 10
        # autocommit must be set to True when using bulk_size
        autocommit = True
        #protocol='json'

def main(host='localhost', port=8086, chunk=100):
    first = True
    chunk_size = chunk

    do_append = True 
    try:
        myclient.create_retention_policy(retention_policy, '3d', 3, default=True)
        print("Create pandas DataFrame")
        df = pd.read_table(sys.stdin, parse_dates=True,index_col=[1],header=0,nrows=30,engine='python')
        names = df.axes[1]
        #print df.axes
        #print names
        #dump(df)
        for row in df.itertuples():
            #print(row)
            [time,mes,proc,subject,info,queue,rcv,drp,prc,tmr,average_wait,average_run,recent_wait,recent_run] = row
            MySeriesHelper(time=time, proc=proc, subject=subject, info=info, queue=queue, rcv=rcv, drp=drp, prc=prc ,tmr=tmr,
                        average_wait=average_wait ,average_run=average_run,recent_wait=recent_wait, recent_run=recent_run)
        while do_append:
            print ("reading more lines")
            df = pd.read_table(sys.stdin, parse_dates=True,index_col=[1],header=None,nrows=20,names=names,engine='python')
            if df.empty:
                print ("Done!")
                do_append = False
                break
            else:
                #dump(more)
                for row in df.itertuples():
                    #print row
                    [time,mes,proc,subject,info,queue,rcv,drp,prc,tmr,average_wait,average_run,recent_wait,recent_run] = row
                    MySeriesHelper(time=time, proc=proc, subject=subject, info=info, queue=queue, rcv=rcv, drp=drp, prc=prc ,tmr=tmr,
                                average_wait=average_wait ,average_run=average_run,recent_wait=recent_wait, recent_run=recent_run)
                print ("Got more?")
            sleep(0.5)
        #print MySeriesHelper._json_body_()
        MySeriesHelper.commit()
    except Exception as inst:
        print (type(inst))
        print (inst.args)
        print (inst)
        print (__file__, 'Oops')

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
        print (type(inst))
        print (inst.args)
        print (inst)
        print (__file__, 'Oops')
