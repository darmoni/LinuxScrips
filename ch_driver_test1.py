#!/usr/bin/env python
from clickhouse_driver import Client
#import connection
import ConfigParser as configparser
import log
from connection import Connection

file_config = configparser.ConfigParser()
file_config.read(['setup.cfg'])

log.configure(file_config.get('log', 'level'))

host = file_config.get('db', 'host')
port = file_config.getint('db', 'port')
database = file_config.get('db', 'database')
user = file_config.get('db', 'user')
password = file_config.get('db', 'password')
compression=file_config.get('db', 'compression') 
#print (host, port, database, user, password)
client = Client(host=host, database=database, user=user, password=password,compression=compression)

print(client.execute('SHOW TABLES;'))

#client.execute('DROP TABLE IF EXISTS test')

client.execute('CREATE TABLE test (x Int32) ENGINE = Memory')

client.execute(
    'INSERT INTO test (x) VALUES',
    [{'x': 1}, {'x': 2}, {'x': 3}, {'x': 100}]
)
client.execute('INSERT INTO test (x) VALUES', [[200]])

print(client.execute('SELECT sum(x) FROM test'))
