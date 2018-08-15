#!/usr/bin/env python



'''
from https://dev.mysql.com/doc/connector-python/en/connector-python-tutorial-cursorbuffered.html

from __future__ import print_function

from decimal import Decimal
from datetime import datetime, date, timedelta

import mysql.connector

# Connect with the MySQL Server
cnx = mysql.connector.connect(user='scott', database='employees')

# Get two buffered cursors
curA = cnx.cursor(buffered=True)
curB = cnx.cursor(buffered=True)

# Query to get employees who joined in a period defined by two dates
query = (
  "SELECT s.emp_no, salary, from_date, to_date FROM employees AS e "
  "LEFT JOIN salaries AS s USING (emp_no) "
  "WHERE to_date = DATE('9999-01-01')"
  "AND e.hire_date BETWEEN DATE(%s) AND DATE(%s)")

# UPDATE and INSERT statements for the old and new salary
update_old_salary = (
  "UPDATE salaries SET to_date = %s "
  "WHERE emp_no = %s AND from_date = %s")
insert_new_salary = (
  "INSERT INTO salaries (emp_no, from_date, to_date, salary) "
  "VALUES (%s, %s, %s, %s)")

# Select the employees getting a raise
curA.execute(query, (date(2000, 1, 1), date(2000, 12, 31)))

# Iterate through the result of curA
for (emp_no, salary, from_date, to_date) in curA:

  # Update the old and insert the new salary
  new_salary = int(round(salary * Decimal('1.15')))
  curB.execute(update_old_salary, (tomorrow, emp_no, from_date))
  curB.execute(insert_new_salary,
               (emp_no, tomorrow, date(9999, 1, 1,), new_salary))

  # Commit the changes
  cnx.commit()

cnx.close()


for desc in result.description:
    colname = desc[0]
    coltype = desc[1]
    print("Column {} has type {}".format(
        colname, FieldType.get_info(coltype)))


Mysql Connection
SQLAlchemy URI looks like this : 'mysql+mysqlconnector://user:password@host_ip:port/database'



'''

import ConfigParser as configparser
import log
#from connection import Connection
import signal
from nested_print import dumpclean,dump,deepdive
from mysql.connector import (connection)
from mysql.connector import FieldType
from sqlalchemy import create_engine
import mysql.connector
import pandas as pd
resources=[]



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
            print type(inst)
            print inst.args
            print inst
            print __file__, 'Oops'
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


'''
use case
CDR=95888664c533e92782d904725d9a441f-534945311@38.102.250.165
sipuri:             vm-voicemail-270-18477165129@75.145.154.234
from:               2244563400@38.102.250.60 (WIRELESS CALLER)
xrefCallId:         1493971941_130931155@67.231.5.176
Leg::loadHasVideo() called. m_hasVideo_loaded=1
    hasVideo:           no
    video streams:      0
    fromAccount in CDR: 0
    toAccount in CDR:   270
Leg::loadHasVideo() called. m_hasVideo_loaded=1


[66163] 10:29:19.774189 [MAPP] <5114> <T9840> [     :     :       ] Call::setup
[66163] 10:29:19.774387 [MAPP] <5114> <T9840> [     :     :       ]     cdr=33455
[66163] 10:29:19.774407 [MAPP] <5114> <T9840> [     :     :       ]     masterAccount=270
[66163] 10:29:19.774420 [MAPP] <5114> <T9840> [     :     :       ]     sipToUser=8477165129
[66163] 10:29:19.774434 [MAPP] <5114> <T9840> [     :     :       ]     sipFromUser=2244563400
[66163] 10:29:19.774447 [MAPP] <5114> <T9840> [     :     :       ]     sipFromHost=38.102.250.60
[66163] 10:29:19.774461 [MAPP] <5114> <T9840> [     :     :       ]     sipFromDisplayName=WIRELESS CALLER
[66163] 10:29:19.774475 [MAPP] <5114> <T9840> [     :     :       ]     fromAccount=0
[66163] 10:29:19.774490 [MAPP] <5114> <T9840> [     :     :       ]     fromPhoneAccount=0
[66163] 10:29:19.774929 [MAPP] <5114> <T9840> [     :     :       ] Account::getOption() accountId=270 name='useGlobalMenuStack' result=''
[66163] 10:29:19.775103 [MAPP] <5114> <T9840> [     :     :       ] LegConversation::LegConversation for leg=0
[66163] 10:29:19.775124 [MAPP] <5114> <T9840> [     :     :       ] Call::start firstLeg=1F2880B0 m_firstConversation=1F28B4D0
[66163] 10:29:19.775140 [MAPP] <5114> <T9840> [     :     :       ] Looking for CallType for vm-voicemail-270-18477165129
[66163] 10:29:19.775157 [MAPP] <5114> <T9840> [     :     :       ] CallType Voicemail
[66163] 10:29:19.775193 [MAPP] <5114> <T9840> [     :     :       ] AccountCall::prepare account=270
[66163] 10:29:19.775207 [MAPP] <5114> <T9840> [     :     :       ] AccountCall::prepare masterAccount=270
[66163] 10:29:19.776026 [MAPP] <5114> <T9840> [     :     :       ] SomeonesLogic::SomeonesLogic account 15118
[66163] 10:29:19.776341 [MAPP] <5114> <T1536> [CNV01:     :       ] Conversation::svc() starts
[66163] 10:29:19.776647 [MAPP] <5114> <T1536> [CNV01:     :       ] Logic::init name=Logic_Menu leg:0 account:15118 (Chicago Office) m_player=0x1f296300, m_ensurePrivateMediaOnInit=1



GET_CALLID
getAccountByPhone(phone='2244563400' domain='38.102.250.60')
'''

class db_provider_client:
    def __init__(self,cnx,cdr_table):
        self.cnx=cnx
        self.cdr_table=cdr_table
        #print("self.cdr_table=",self.cdr_table)

    def getMenuScheduleById(self, data, schId):
        print ("getMenuScheduleById schId={}".format(schId))
        for sch in data:
            if sch['id'] == schId:
                return sch
        return None

    def getMenuItemSchedule(self,itemIds):
        print("MenuItem_i::getScheduleById(id_type schId)")
        q = "select * from menuitemschedule where itemId in {} order by itemId, `option`".format(itemIds)
        return self.select_this(q,None,True)

    def getMenuItems(self,menuId):
        q = "select * from menuitem where menuId={} order by orderValue".format(menuId)
        return self.select_this(q,None,True)
#menuId=my_db_provider.select_this('select id from menudata where accountId={}'.format(mainMenuAccountId))['id'][0]

    def getMenuId(self,mainMenuAccountId):
        q = 'select id from menudata where accountId={}'.format(mainMenuAccountId)
        return self.select_this(q,None,True)['id'][0]

    def getMainMenuAccountId(self,toAccountid):
        q = 'select mainMenuAccountId from account where id = {}'.format(toAccountid)
        return self.select_this(q,None,True)['mainMenuAccountId'][0]

    def getCdrByCallId(self,call_id):
        q=("select id, cacheCdrId, toAccountid, fromAccountid, fromUser, fromDomain from {} where call_id='{}'").format(self.cdr_table,call_id)
        return self.select_this(q,None,True)['id'][0]

    def startForCallId(self,call_id,description):
        #print("{},{}".format(call_id,description))
        return self.getCdrByCallId(call_id)

    def select_this(self,q,params=None,return_values=False):
        queries = q.split(';')
        if len(queries) > 1:
            df=[]
            for q in queries:
                if q:
                    print(q)
                    df.append(pd.read_sql(q, self.cnx))
            if 1 == len(df):
                return df[0]
            # ====== Reading table ====== #
            # Reading Mysql table into a pandas DataFrame
            #df = pd.concat([pd.read_sql(q, self.cnx) for q in queries])
        elif len(queries) > 0:
            print(q)
            df = pd.read_sql(q, self.cnx)
        return df



def setupCall(callId,description=None):
    data=my_db_provider.startForCallId(callId,description)
    cdrId=data
    data=my_db_provider.select_this(('select * from callrecords where id={}'.format(cdrId)),None)
    data.style
    #print(data.to_html())
    #exit(0)
    fieldNames=list(data.columns.values)
    for fname in fieldNames:
        if isinstance(data[fname][0], basestring):
            print("{}='{}'".format(fname,data[fname][0]))
        else:
            print("{}={}".format(fname,data[fname][0]))
    #exit(0)
    toAccountid=data['toAccountid'][0]
    mainMenuAccountId=my_db_provider.getMainMenuAccountId(toAccountid)
    print(mainMenuAccountId)

    menuId=my_db_provider.getMenuId(mainMenuAccountId)#['id'][0]
    #print("menuId =",menuId)

    data = my_db_provider.getMenuItems(menuId).get_values()
    ids=[]
    for row in data:
        ids.append(row[0])
    data = my_db_provider.getMenuItemSchedule(tuple(ids))
    if len(data) < 1 :
        print("********** Got no menuitemschedule for this account, using 1224 for debug **********")
        ids.append(1224)
        data = my_db_provider.getMenuItemSchedule(tuple(ids))
    #data.style.format("{:.2%}")
    #print(data)
    #data.style#.highlight_null()#.render()#.split('\n')
    print(data)
    #print(data.to_html())
    #print (my_db_provider.select_this("select * from menuitemschedule where itemId in {} order by itemId, `option`".format(tuple(ids))))
    #exit(0)
    '''
    # Mutiple Queries
    q="SHOW TABLES;SELECT id, accountId, optionId, value, startDate, endDate, version FROM accountoptions WHERE optionId = {} limit {}"
    #q="SELECT id, accountId, optionId, value, startDate, endDate, version FROM accountoptions WHERE optionId = {} limit {}"
    test_optionId = 324
    dummy_notused = 500
    q_limit = 3
    data = my_db_provider.select_this(q.format(test_optionId,2),None)
    for res in data:
        print(res)

    data = my_db_provider.select_this("select * from recording_fragment_mapp where compId=(select id from recording_composition_mapp where name='{}' and language = '{}') order by orderValue limit {}".format('messages-options','English',25))
    print(data)
    data = my_db_provider.select_this("select * from recording_fragment_mapp where compId=(select id from recording_composition_mapp where name='{}' and language = '{}') order by orderValue limit {}".format('time','English',25))
    print(data)
    '''

if __name__ == '__main__':
    file_config = configparser.ConfigParser()
    file_config.read(['xcast_sql.cfg'])
    log.configure(file_config.get('log', 'level'))

    #port = file_config.getint('db', 'port')
    #print (host, port, database, user, password)
    db_config = {
    'user': file_config.get('db', 'user'),
    'password': file_config.get('db', 'password'),
    'host': file_config.get('db', 'host'),
    'database': file_config.get('db', 'database'),
    'raise_on_warnings': True,
    }
    #print (db_config)
    system_type=file_config.get('mode', 'system_type');
    tbl_recording_fragment=file_config.get(system_type,'tbl_recording_fragment')
    tbl_recording_composition=file_config.get(system_type,'tbl_recording_composition')
    cdr_table=file_config.get('mode', 'cdr_table')
    #print(cdr_table,system_type,tbl_recording_fragment,tbl_recording_composition)

    try:
        #print("main:")
        try:
            # ====== Connection ====== #
            #SQLAlchemy URI looks like this : 'mysql+mysqlconnector://user:password@host_ip:port/database'
            # Connecting to mysql by providing a sqlachemy engine
            engin_param='mysql+mysqlconnector://{}:{}@{}:3306/{}'.format(db_config['user'],db_config['password'],db_config['host'],db_config['database'])
            engine = create_engine(engin_param, echo=False)
            #cnx = connection.MySQLConnection(**db_config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        except Exception as inst:
            print type(inst)
            print inst.args
            print inst
            print __file__, 'Oops'

        resources.append(engine)
        #print(engine)
        my_db_provider=db_provider_client(engine,cdr_table)
        callId='95888664c533e92782d904725d9a441f-534945311@38.102.250.165'
        description='''
                    m_baseCdr = (callId!=0 && *callId!='\0') ? AccountFactory_i::getInstance()->loadCdrByCallId(callId, false) : 0;
        if (m_baseCdr!=0)
        {
                m_logTag.assign(m_baseCdr->logTag());
                m_eventTag.assign(m_baseCdr->eventTag());

                m_baseCdr->registerHandler(this);

                LogMarker_Call logMarker(this);
                LogEvent("APP%08d START %s\n", m_id, description);
        }
            '''
        #dumpclean ("call_id = {}".format())
        setupCall('95888664c533e92782d904725d9a441f-534945311@38.102.250.165')
#        resources.remove(cnx)
        safe_exit()
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        print __file__, 'Oops'
    safe_exit()
    exit(0)

