#!/usr/bin/env python2

'''
$Id$

from https://dev.mysql.com/doc/connector-python/en/connector-python-tutorial-cursorbuffered.html
'''

import ConfigParser as configparser
#import configparser
import log
import signal
from sqlalchemy import create_engine
import pandas as pd
resources=[]

def safe_exit():
    counter=0
    for r in resources:
        try:
            counter += 1
            resources.remove(r)
            if None == r:
                continue
            print("deleted {} {}".format(counter, r))
            del r
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print(__file__, 'Oops')
            continue
    exit(0)

def sig_handler(sig, frame):
    print ("got sig(%d)\n" % sig)
    safe_exit()

signal.signal(signal.SIGUSR1, sig_handler)
signal.signal(signal.SIGUSR2, sig_handler)
signal.signal(signal.SIGINT, sig_handler)
signal.signal(signal.SIGTERM, sig_handler)
signal.signal(signal.SIGHUP, sig_handler)

class MenuItemType:
    MITchoice = 0
    MITtimeout = 1

class MenuActionType:
    MATnoAction = 0
    MATgoBack = 1
    MATgoHome = 2
    MATcallToAccount = 3
    MATcallToPhone = 4
    MATleaveMessage = 5
    MATcheckMessages = 6

    MATcallToCalleeAccount = 6
    MATleaveMessageForCallee = 7
    MATcheckCalleeMessages = 8

class AccountType:

    ATany = 0 #/// 0 Any type - used in requests
    ATextension = 1 #           /// 1 Phone extension (can accept registrations of sip phones and serve as a transfer destination,
                            #   ///  can not do much else
    ATuser = 2  #     /// 2 User account
    ATgroup = 3 #     /// 3 Group account - sales, CS and the like
    ATpbx = 4   #   /// 4 PBX account (corporation) <future extension!>
    ATroot = 5  #   /// 5 root account
    ATqueue = 6 #   /// 6 ACD account=
    ATmenu = 7  #   /// 7 menu account
    ATcard = 8  #   /// 8 card account
    ATintercom = 9  #   /// 9 intercom account
    ATreseller = 10 #   /// 10 reseller account
    ATcallGroup = 11    #   /// 11 call group account
    ATconference = 12   #   /// 12 conference account
    ATdialerDialog = 13 #   /// 13 dialer dialg
    ATtrunkGroup = 12   #   /// 14 trunk group
    ATvideo = 15    #    /// 15 video server
    ATgateway = 16    #    /// 16 gateway enterance - dialing any number
    ATdivision = 17    #    /// 17 division
    ATsharedLine = 18    #    /// 18 shared line
    ATxDialer = 19    #    /// 19 XDial service
    ATpsapGroup = 20    #    /// 20 PSAP group



class db_provider_client:

    def __init__(self, cnx):
        self.cnx=cnx

    def select_this(self, q, params=None, return_values=False):
        queries = q.split(';')
        if len(queries) > 1:
            df=[]
            for q in queries:
                if q:
                    print(q+';')
                    df.append(pd.read_sql(q, self.cnx))
            if 1 == len(df):
                return df[0]
            # ====== Reading table ====== #
            # Reading Mysql table into a pandas DataFrame
            #df = pd.concat([pd.read_sql(q, self.cnx) for q in queries])
        elif len(queries) > 0:
            print(q+';')
            df = pd.read_sql(q, self.cnx)
        return df


def print_table_data(data, included = []):
    #return
    print("len(included) = {}".format(len(included)))
    #print(data)
    fieldNames = list(data.columns.values)
    print(fieldNames)
    if 0 < len(included):
        for fname in included:
            if isinstance(data[fname][0], basestring):
                print("{}='{}'".format(fname, data[fname][0]))
            else:
                print("{}={}".format(fname, data[fname][0]))
    else:
        for fname in fieldNames:
            if isinstance(data[fname][0], basestring):
                print("{}='{}'".format(fname, data[fname][0]))
            else:
                print("{}={}".format(fname, data[fname][0]))

    #print('Done')
tables = {}
def set_table_params(name, max_number_of_fields = 945, max_discrete_values =15):
    tables.update({
        name:{
            'number_of_fields':max_number_of_fields,
            'discrete_values':max_discrete_values
            }
        })


if __name__ == '__main__':
    file_config = configparser.ConfigParser()
    file_config.read(['xcast_broker_sql.cfg'])
    log.configure(file_config.get('log', 'level'))

    db_config = {
    'user': file_config.get('db', 'user'),
    'password': file_config.get('db', 'password'),
    'host': file_config.get('db', 'host'),
    'database': file_config.get('db', 'database'),
    'raise_on_warnings': True,
    }
    #print (db_config)
    #exit(0)

    explore_db = {
        'tables':file_config.get('db', 'tables').replace(',','\n'),
    }

    #print(explore_db['tables'])
    #exit(0)

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
            print(type(inst))
            print(inst.args)
            print(inst)
            print(__file__, 'Oops')
            safe_exit()

        resources.append(engine)
        #print(engine)
        nl = "\n"
        valid_tables = explore_db['tables'].split()
# set default settings
        for table_name in valid_tables:
            set_table_params(table_name)

# exceptions are allowed
        set_table_params('AccessClasses', 10, 15)

        db_connection=db_provider_client(engine)
        q = 'SHOW TABLES'
        try:
            data = db_connection.select_this(q)
            for row in data.get_values():
                table = row[0]
                if table not in valid_tables:
                    #print("ohoh, `{}` not found in valid_tables".format(table))
                    continue
                table_q = "SHOW FIELDS FROM `{}`".format(table)
                try:
                    table_data = db_connection.select_this(table_q)
                    field_counter = 0
                    for row in table_data.get_values():
                        if tables[table]['number_of_fields'] <= field_counter:
                            break
                        field_counter += 1
                        field = row[0]
                        #print("`{}`".format(field))
                        field_q = "SELECT DISTINCT `{}` FROM `{}` ORDER BY `{}` LIMIT {}".format(field, table, field, tables[table]['discrete_values'])
                        try:
                            fields_data = db_connection.select_this(field_q)
                            if 0 == len(fields_data):
                                continue
                            value_counter = 0
                            for row in fields_data.get_values():
                                value = row[0]
                                value_counter += 1
                                print("{:-4}: `{}`= {}".format(value_counter, field,value))
                            print(nl)
                        except:
                            continue
                    print(nl)
                except:
                    continue
        except:
            exit(0)
        safe_exit()
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)
        print(__file__, 'Oops')
    safe_exit()
    exit(0)
