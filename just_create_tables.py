#!/usr/bin/env python
from middle_event_structure import Xcast_event_table
from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname
MAX_SIZE=4096
import time, sys, re
from Queue import Queue
from threading import Thread

from clickhouse_driver import Client
import ConfigParser as configparser
import log
from connection import Connection
import signal

resources=[]
def safe_exit():
    for r in resources:
        del r
    exit(0)

def sig_handler(sig, frame):
    print ("got sig(%d)\n" % sig)
    safe_exit()

signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)

#print(client.execute('SHOW TABLES;'))


if __name__ == '__main__':
    file_config = configparser.ConfigParser()
    file_config.read(['setup.cfg'])
    log.configure(file_config.get('log', 'level'))
    
    host = file_config.get('db', 'host')
    #port = file_config.getint('db', 'port') using default port
    database = file_config.get('db', 'database')
    user = file_config.get('db', 'user')
    password = file_config.get('db', 'password')
    compression=file_config.get('db', 'compression') 
    #print (host, port, database, user, password)
    middle_prefix='middle_'
    table_name='test'
    try:
        print("main:")
        my_dos=Xcast_event_table(['',''],'testing',middle_prefix)
        print (my_dos.print_table(middle_prefix+table_name))
        Xcast_event_table.xcast_event_tables.clear()
        my_dos=Xcast_event_table(['',''],'ddos',middle_prefix,True)
        print (my_dos.print_table(middle_prefix+table_name))
        Xcast_event_table.xcast_event_tables.clear()
        my_dos=Xcast_event_table(['',''],'testing',middle_prefix,False)
        print (my_dos.print_table(middle_prefix+table_name))

        safe_exit()
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        print __file__, 'Oops'
    safe_exit()
