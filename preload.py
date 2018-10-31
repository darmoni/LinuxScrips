#!/usr/bin/env python3

# $Id$ $Date$


#from threading import Thread
#from queue import Empty, Queue
#import signal, time

#import ACD_pb2, sys, os
import os.path
import sys, argparse
import pandas as pd
#import ConfigParser as configparser
import configparser
import MySQLdb as mysql#import _mysql as mysql
from MySQLdb.constants import FIELD_TYPE
#from _mysql import _mysql_exceptions
import signal

from PreLoadUtils import preload, make_xlat_re


def safe_exit():
    counter=0
    for r in resources:
        try:
            counter+=1
            resources.remove(r)
            if None == r:
                continue
            print("deleted {} {}".format(counter,r))
            del r
        except Exception as inst:
            print (type(inst))
            print (inst.args)
            print (inst)
            print (__file__, 'Oops')
            continue
    exit(0)

def sig_handler(sig, frame):
    print ("got sig(%d)\n" % sig)
    safe_exit()

signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)


def main(db_config, table_name, StartuctName):

    table_filter = {
        "\n":None,
        "\|":'\t',
        "(varchar(.+))": 'std::string',
        "(char(.+))": 'std::string',
        "double":'double_t',
        "(tinyint\(d+\))":'uint32_t',
        "(int\(\d\))":'uint32_t',
        "(int\(\d+\))":'int64_t',
        "int64_t unsigned":'uint64_t',
        "int32_t unsigned":'uint32_t',
        "tinyuint32_t":'uint32_t'
        }
    transre = make_xlat_re(**table_filter)
    '''
    print(transre.rx)
    print(transre(transre("int(11) int(11) unsigned tinyint(3)")))
    exit(0)
    '''
    names = []
    name_type = {}    #print(name_type)
    #table_filter = {'\n':None,'|':'\t','double':'double_t','tinyint(d+)':'uint32_t','int(\d+) unsigned':'uint64_t','int(\d+) unsigned':'uint64_t','int(\d+)':'int64_t','int(\d+)':'uint32_t'}#,s1:'std::string'}
    #showfields_filter= make_xlat(**table_filter)

    db = mysql.connect(db_config['host'], db_config['user'], db_config['password'], db_config['database'])

    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    try:
        cursor.execute("SHOW FIELDS FROM {}".format(table_name))
        results = cursor.fetchall()
        for row in results:
            #print("{} {}".format(row[0], row[1]))
            name_type[row[0]] = transre(row[1])
            names.append(row[0])
        cursor.close()
        preloader = preload()
        print(preloader.define_structure(names, name_type, StartuctName, table_name))
        select_command_ = preloader.select_command(names, table_name)
        #print(select_command)
        assign_command_ = preloader.assign_command(names, name_type)
        #print((names, name_type, StartuctName, table_name))
        print(preloader.declarations(names, name_type, StartuctName, table_name, assign_command_, select_command_))
        return 0
    except:
        print("Error: unable to fetch data")
    # disconnect from server
        if db:
            db.close()
    exit(1)

def parse_args():
    mydir=os.path.dirname(__file__)
    parser = argparse.ArgumentParser(
        description='Automatic c++ Code generator for a defined MYSQL table name')
    parser.add_argument('--table_name', type=str, required=False,
                        default='queue_records',
                        help='MYSQL table name')
    parser.add_argument('--conf', type=str, required=False,
                        default=mydir+'/preload_sql.cfg',
                        help='Config File name')
    return parser.parse_args()


if __name__ == '__main__':

    args = parse_args()
    file_config = configparser.ConfigParser()
    if os.path.isfile(args.conf):
        file_config.read([args.conf])

    #port = file_config.getint('db', 'port')
    #print (host, port, database, user, password)
    db_config = {
    'user': file_config.get('db', 'user'),
    'password': file_config.get('db', 'password'),
    'host': file_config.get('db', 'host'),
    'database': file_config.get('db', 'database'),
    'raise_on_warnings': True,
    }
    if args.table_name:
        table_name = args.table_name
    else:
        table_name = file_config.get('db', 'sqltable_name')
    StartuctName=''
    for a in table_name.split('_'):
        StartuctName += a.capitalize()
    main(db_config, table_name, StartuctName)
