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
import sqlite3
from PreLoadUtils import preload, make_xlat_re
import shlex
from subprocess import call, Popen, check_output, PIPE

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

    #db = mysql.connect(db_config['host'], db_config['user'], db_config['password'], db_config['database'])

    # prepare a cursor object using cursor() method
    #cursor = db.cursor()
    try:
        last_id = read_names()
        #return(0)
        write_names(get_names(db_config), last_id)
        read_names()
        return(0)
    except:
        print("OOOOOOOOOOPPPPPSSSSYY")
        #q = "SELECT TABLE_NAME, 'NA', 'NA', 'NA', 3 FROM information_schema.tables"
        #print(q)
        #cursor.execute(q)
        #results = cursor.fetchall()
        '''
       import sqlite3
        conn = sqlite3.connect('example.db')
        c = conn.cursor()

        # Larger example that inserts many records at a time
purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
            ]
c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
# Save (commit) the changes
conn.commit()
conn.close()

t = ('RHAT',)
c.execute('SELECT * FROM stocks WHERE symbol=?', t)
print(c.fetchone())


        print("names = [",end = "")
        names = []
        for row in results:
            #print("('{}', '{}', '{}', '{}', {}),".format(row[0], row[1], row[2], row[3], row[4]))
            name.append((row[0], row[1], row[2], row[3], row[4]))
        cursor.close()
        print("]")
        print("c.executemany('INSERT INTO prepare_choice VALUES (?,?,?,?,?), names)")
        '''
def get_names(db_config):
    print('get_names()')
    db = mysql.connect(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
    q = "SELECT TABLE_NAME,'NA','NA','NA' FROM information_schema.tables "
    cursor = db.cursor()
    try:
        cursor.execute(q)
        results = cursor.fetchall()
        print("get_names LINE 106 ", len(results))
        names = []
        for row in results:
            #print("get_names LINE 109 \n", (row[0], row[1], row[2], row[3]))
            row_names = row[0]#, row[1], row[2], row[3])
            names.append((row_names,))
        cursor.close()
        db.close()
        #print(names)
        return names
    except:
        print('get_names OOOPS')
        return -1

def delete_names(conn, name):
    print('delete_names() ', name)
    try:
        conn.execute("DELETE FROM prepare_choice WHERE `question_id` = 3 AND `choice_path` = '{}'".format(name))
    except Exception as inst:
        print (type(inst))
        print (inst.args)
        print (inst)
        print (__file__, 'Oops')
        safe_exit()

def write_names(names, last_id=0):
    print('write_names')
    try:
        conn = sqlite3.connect('example.db')
        conn.row_factory = sqlite3.Row

        #conn.execute('CREATE TABLE IF NOT EXISTS "prepare_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "question_text" varchar(200) NOT NULL, "pub_date" datetime NOT NULL);')
        #conn.execute('CREATE TABLE IF NOT EXISTS "prepare_choice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "choice_path" varchar(200) NOT NULL, "choice_builder_filename" varchar(200) NOT NULL, "choice_packagename" varchar(200) NOT NULL, "choice_gittagname" varchar(200) NOT NULL, "question_id" integer NOT NULL REFERENCES "prepare_question" ("id") DEFERRABLE INITIALLY DEFERRED);')
        #conn.execute('CREATE INDEX "prepare_choice_question_id_a9cbab19" ON "prepare_choice" ("question_id");')
        audit_cmd = "./preload.py -t '{}'"
        #c = conn.cursor()
        for row in names:
            name = row[0]
            print("NAMES as coming to write_names: {}".format(name))
            args = shlex.split(audit_cmd.format(name))
            try:
                check_output(args)
            except:
                delete_names(conn, name)
                continue

            q = "SELECT `id` FROM `prepare_choice` WHERE `question_id` = 3 AND `choice_path` = '{}'".format(name)
            print(q)
            results = conn.execute(q).fetchone()
            if results:
                print ("Name exists ({}".format(q))
                #last_id -= 1  # reuse the index
                continue
            last_id += 1
            row_names="{}, '{}', 'NA','NA','NA', 3".format(last_id,name)
            q="INSERT INTO prepare_choice VALUES ({});".format(row_names)
            print(q)
            try:
                if 1 > conn.execute(q).rowcount:
                    print ("Not good ({}".format(q))
                    last_id -= 1  # reuse the index
                    continue
            except Exception as inst:
                    print (type(inst))
                    print (inst.args)
                    print (inst)
                    print (__file__, 'Oops')
                    safe_exit()

            except:
                print('write_names exception')
                continue
        #c.executemany("INSERT INTO prepare_choice VALUES (?,?,?,?,?)", names)
        conn.commit()
    except Exception as inst:
            print (type(inst))
            print (inst.args)
            print (inst)
            print (__file__, 'Oops')
            safe_exit()

    except sqlite3.IntegrityError:
        print("couldn't add Joe twice")
        conn.close()
    except:
        print('write_names OOOPS')
        conn.close()
        return -1
    conn.close()
    return 0

def read_names():
    try:
        print('read_names()')
        conn = sqlite3.connect('example.db')
        t = (3,)
        count = conn.execute('SELECT COUNT(*) FROM prepare_choice WHERE question_id=?', t).fetchone()[0]
        print (count)
        #c = conn.cursor()
        results = conn.execute('SELECT id FROM prepare_choice ORDER BY id DESC limit 1').fetchone()
        for row in results:
            print(row)
            last_id = int(row)
        print (last_id)
        #print(c.fetchone())
        '''
        c = conn.cursor()
        c.executemany('INSERT INTO prepare_choice VALUES (?,?,?,?,?)', names)
        conn.commit()
        '''
        conn.close()
        return(last_id)

    except Exception as inst:
            print (type(inst))
            print (inst.args)
            print (inst)
            print (__file__, 'Oops')
            safe_exit()
    except:
        print('OOOPS')
        return -1

def parse_args():
    mydir=os.path.dirname(__file__)
    parser = argparse.ArgumentParser(
        description='Automatic c++ Code generator for a defined MYSQL table name')
    parser.add_argument('-t', '--table_name', type=str, required=False,
                        default='queue_records',
                        help='MYSQL table name')
    parser.add_argument('-c', '--conf', type=str, required=False,
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
