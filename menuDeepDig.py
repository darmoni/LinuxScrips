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



'''
Business logic from mapp/menu.cpp

Logic* MenuItem::createLogicByAccount(Account* account)
{
//      MAPP_DEBUG((LM_TRACE, "MenuItem_Dial::addPrompt() greeting found\n" ));

        Logic* result = 0;
        if (account!=0)
        {
                if (account->menuAccountId()==0)
                {
                        switch (account->type())
                        {
                        case XCast::ATuser:
                                result = new Logic_Guest(menuCall(), account, menuPlayer(), menuCallingLeg());
                                break;
                        case XCast::ATpbx:
                                result = new Logic_Pbx(menuCall(), account, menuPlayer(), menuCallingLeg());
                                break;
                        case XCast::ATcallGroup:
                                result = new Logic_LeaveVoicemailForCallGroup(menuCall(), account, menuPlayer(), menuCallingLeg());
                                break;
                        case XCast::ATsharedLine:
                                result = new Logic_LeaveVoicemailForSharedLine(menuCall(), account, menuPlayer(), menuCallingLeg());
                                break;
                        case XCast::ATqueue:
                                result = new Logic_AcdExterior(menuCall(),
                                        *AcdContext::create(menuCall(), account),
                                        menuPlayer(), menuCallingLeg());
                                break;
                        case XCast::ATmenu:
                                result = new Logic_Menu(menuCall(),
                                        m_menu->menuUserAccount(),
                                        account, menuPlayer(), menuCallingLeg(), "");
                                break;
                        case XCast::ATconference:
                                {
                                        result = new Logic_ConferenceEnterance(menuCall(),
                                                *ConferenceContext::create(menuCall(), account),
                                                account, menuPlayer());
                                        break;
                                }
                        default:
                                break;
                        }
                }
                else
                {
                        Account* menuAccount = AccountStore::instance()->findAccount(account->menuAccountId());
                        if (menuAccount!=0 && menuAccount->type()==XCast::ATmenu)
                                result = new Logic_Menu(menuCall(),
                                        m_menu->menuUserAccount(),
                                        menuAccount, menuPlayer(), menuCallingLeg());
                }
        }
        return result;
}

'''

class db_provider_client:

    def __init__(self, cnx, cdr_table):
        self.cnx=cnx
        self.cdr_table=cdr_table
        print("self.cdr_table=",self.cdr_table)

    def getParentIdByDomain(self, domain):
        print ("getParentIdByDomain({})".format(domain))
        q = "SELECT DISTINCT `ParentId` FROM `account` WHERE `type` = 7 AND `domain` ='{}' ORDER BY id".format(domain)
        return self.select_this(q, None)

    def getMenuItemSchedule(self, itemIds):
        #print("getMenuItemSchedule(id_type schId. itemIds = ({}))".format(", ".join(itemIds)))
        if 0 < len(itemIds):
            #print("getMenuItemSchedule(id_type schId. itemIds = ({}))".format(", ".join(itemIds)))
            q = "SELECT * FROM `menuitemschedule` WHERE `itemId` IN ({}) ORDER BY `itemId`, `option`".format(", ".join(itemIds))
            data = self.select_this(q, None, True)
            #print(data)
            return data
        return ('')

    def getMenuItems(self, menuId):
        q = "SELECT * FROM `menuitem` WHERE `menuId` = {} ORDER BY `orderValue`".format(menuId)
        return self.select_this(q, None, True)

    def getMenuId(self,mainMenuAccountId):
        q = 'SELECT `id` FROM `menudata` WHERE `accountId` = {}'.format(mainMenuAccountId)
        return self.select_this(q, None, True)['id'][0]

    def getMainMenuAccountId(self,toAccountid):
        q = 'SELECT `mainMenuAccountId` FROM `account` WHERE `id` = {}'.format(toAccountid)
        return self.select_this(q, None, True)['mainMenuAccountId'][0]

    def getCdrByCallId(self,call_id):
        q=("SELECT `id`, `cacheCdrId`, `toAccountid`, `fromAccountid`, `fromUser`, `fromDomain` FROM {} WHERE `call_id` = '{}'").format(self.cdr_table, call_id)
        return self.select_this(q, None, True)['id'][0]

    def startFromCallId(self, call_id, description):
        print("{}, {}".format(call_id, description))
        return self.getCdrByCallId(call_id)

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

    def getMyPbxAccountId(self, account):
        q = 'SELECT `type`, `parentId` FROM `account` WHERE `id` = {};'.format(account)
        data = self.select_this(q, None, True)
        print(data)
        type = data['type'][0]
        print("type = {}".format(type))
        if 4 == type :
            return (account)
        pId = data['parentId'][0]
        return self.getMyPbxAccountId(pId)

    def getTimeZone(self, account):
        pId = self.getMyPbxAccountId(account)
        q = 'SELECT `id`, `timeZone`, `accountId` FROM `companydata` WHERE `accountId` = {};'.format(pId)
        data = self.select_this(q, None, True)
        print(data)

def mainMenuDrillIn(mainMenuAccountId):
    print(mainMenuAccountId)

    menuId = db_connection.getMenuId(mainMenuAccountId)#['id'][0]
    print("menuId = {}".format(menuId))

    data = db_connection.getMenuItems(menuId)#.get_values()
    ids = []
    idsWithTypeMITtimeout = []        # might have schedule info in menuitemschedule
    #print(data)
    print_table_data(data,['id','type'])
    for row in data.get_values():
        ids.append(str(row[0]))
        menuItemType = row[2]
        if MenuItemType.MITtimeout == menuItemType:
            idsWithTypeMITtimeout.append(str(row[0]))
    print(idsWithTypeMITtimeout)
    # get Schedules, if exist
    schedData = db_connection.getMenuItemSchedule(tuple(idsWithTypeMITtimeout))
    if 0 < len(schedData):
        tz = db_connection.getTimeZone(mainMenuAccountId)
        print(schedData)

    print("mainMenuDrillIn itemIds = {}".format(", ".join(ids)))
    print("Done")

def print_table_data(data, included = []):
    #return
    print("len(included) = {}".format(len(included)))
    #print(data)
    fieldNames = list(data.columns.values)
    #print(fieldNames)
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

def setupCall(callIds, domains, description = None):
    if len(domains) > 0:
        for domain in domains:
            print('\nDrilling down from Domain Information')
            print("\ndomain = '{}'".format(domain))
            data = db_connection.getParentIdByDomain(domain)
            print_table_data(data)
            parentId = data['ParentId'][0]
            #print(parentId)

            mainMenuAccountId=db_connection.getMainMenuAccountId(parentId)
            db_connection.getTimeZone(parentId)
            mainMenuDrillIn(mainMenuAccountId)

    if len(callIds) > 0:
        for callId in callIds:
            print('\nDrilling down from callIds Information')
            print("\ncallId = '{}'".format(callId))
            data = db_connection.startFromCallId(callId, description)
            cdrId = data
            data = db_connection.select_this(('SELECT * FROM {} WHERE `id` = {}'.format(db_connection.cdr_table, cdrId)), None)
            #print_table_data(data)
            toAccountid=data['toAccountid'][0]
            db_connection.getTimeZone(toAccountid)
            mainMenuAccountId=db_connection.getMainMenuAccountId(toAccountid)
            mainMenuDrillIn(mainMenuAccountId)

if __name__ == '__main__':
    file_config = configparser.ConfigParser()
    file_config.read(['xcast_sql.cfg'])
    log.configure(file_config.get('log', 'level'))

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
            print(type(inst))
            print(inst.args)
            print(inst)
            print(__file__, 'Oops')
            safe_exit()

        resources.append(engine)
        #print(engine)
        db_connection=db_provider_client(engine, cdr_table)
        callId='95888664c533e92782d904725d9a441f-534945311@38.102.250.165'

        setupCall(('8c3b624ec1c1f9b9633ebafa41218ab2-51945071@38.102.250.163', callId), ('siptalk64.xcastlabs.com', 'russ.xcastlabs.com'))
        safe_exit()
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)
        print(__file__, 'Oops')
    safe_exit()
    exit(0)
