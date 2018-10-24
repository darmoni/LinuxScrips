#!/usr/bin/env python

# $Id$ $Date$


#from threading import Thread
#from queue import Empty, Queue
#import signal, time

#import ACD_pb2, sys, os
import sys, re

def template(template, place_holder, seed):
    return template.replace(place_holder,seed)


variable_template ='''
// Place in XXXService.hpp:

typedef std::map<ID_t, {}_t>    M{}_t;

mutable RW_Mutex                M{}Lock_m;
std::unique_ptr<M{}_t>			PM{}_m;
'''


read_from_sql_template = '''
    std::unique_ptr<M{}_t>  pM{}(new M{}_t);
    ID_t parent_id, account_id;
    int col;
    while( dbc->NextRow() ) {
        col=0;
        parent_id = atol(STR(dbc->RValue(1)));
        account_id = atoi( STR(dbc->RValue()));
        if(parent_id && account_id)
            pbxIdOfId(account_id,parent_id);                                        // update PbxId table
        pM{}->emplace( M{}_t::value_type( account_id ,{           // key is account_id
            (ID_t) atoi( STR(dbc->RValue())),           // account_id
            (ID_t) atoi( STR(dbc->RValue(++col))),      // parent_id
            (std::string ) STR(dbc->RValue(++col)),     // phone_number
            (time_t) atoll(STR(dbc->RValue(++col))),    // hard_login_time
            (time_t) atoll(STR(dbc->RValue(++col))),    // soft_login_time
            (time_t) atoll(STR(dbc->RValue(++col))),    // hard_logoff_time
            (time_t) atoll(STR(dbc->RValue(++col))),    // soft_logoff_time
            (uint32_t) atoll(STR(dbc->RValue(++col))),  // unanswered_calls_limit
            (uint32_t) atol(STR(dbc->RValue(++col))),   // unanswered_calls_cnt
            (time_t) atoll(STR(dbc->RValue(++col))),    // next_call_can_start
            (time_t) atoll(STR(dbc->RValue(++col))),    // last_call_end_time
            (uint32_t) atol(STR(dbc->RValue(++col))),   // calls_served
            (uint32_t) atol(STR(dbc->RValue(++col))),   // is_queue_supervisor
            (time_t) atoll(STR(dbc->RValue(++col))),    // last_call_assigned_time
            (bool) atol(STR(dbc->RValue(++col))),       // login_status`
            (std::string) STR(dbc->RValue(++col)),      // call_status,
            (std::string) STR(dbc->RValue(++col))       // last_phone_number,
        } ) );
    }
    Log(QMANS, QMANS_DEBUG, "Loaded {}: %zu, last column: %u \\n", pM{}->size(),col);
    Log(QMANS, QMANS_DEBUG, "   (Updated PMPbxIds_m: %zu)\\n", PMPbxIds_m->size());

    M{}Lock_m.write_lock();
    PM{}_m.swap(pM{});
    M{}Lock_m.unlock();
}
'''

def from_QueueMan_i_to_QmanService(corba_qman_code, seed):
    adict ={'{}':seed,'ACE_DEBUG':'Log',
        'ANT(row[i++]':'STR(dbc->RValue(++col)',
        'row[0]': 'dbc->RValue()',
        'MYSQL_ROW row;':'''
    int n = dbc->Query(os.str());
    if( n <= 0 ) {
    Log(QMANS, QMANS_ERROR, "ERROR: Preload() Cannot retrive 'YOUR TABLE NAME HERE'\\n");
    return false;
    }
    int col;
    ''',
    'if((row = q.fetch_row()) != NULL)':'\twhile( dbc->NextRow() )',
    'int i = 0;':''
        }
    #print(adict)

    temp=corba_qman_code
    corba2vg = make_xlat(**adict)
    print (corba2vg(corba_qman_code))
    '''
    for key in adict.keys():
        temp = temp.replace(key,adict[key])
    print(temp)
'''
#print_template(read_from_sql_template, 'STR(dbc->RValue(++col)','ANT(row[i++]')
#print_template(corba_qman_code,'ANT(row[i++]', 'STR(dbc->RValue(++col)')
#print_template(variable_template,'{}', 'QueueData')

def main(argv):
    variable_template ='''
// Place in XXXService.hpp:

typedef std::map<ID_t, {}_t>    M{}_t;

mutable RW_Mutex                M{}Lock_m;
std::unique_ptr<M{}_t>			PM{}_m;
'''

    corba_qman_code = '''

    // Place in XXXService.cpp:

    bool Acd_Queue_i::init(DbQuery& q)
    {
    MYSQL_ROW row;
    if((row = q.fetch_row()) != NULL)
        {
        int i = 0;
        if(!row[0])
            return false;
        account_id_ = atol(ANT(row[i++]));
        name_ = ANT(row[i++]);
        strategy_ = ANT(row[i++]);
        announce_frequency_ = atol(ANT(row[i++]));
        announce_hold_time_ = atol(ANT(row[i++]));
        timeout_ = atol(ANT(row[i++]));
        retry_ = atol(ANT(row[i++]));
        maxlen_ = atol(ANT(row[i++]));
        wrapuptime_ = atol(ANT(row[i++]));
        penalty_ = atof(ANT(row[i++]));
        overflow_account_id_ = atol(ANT(row[i++]));
        overflow_action_ = ANT(row[i++]);
        parent_id_ = atol(ANT(row[i++]));
        on_digit_action_while_waiting_ = atol(ANT(row[i++]));
        waiting_menu_id_ = atol(ANT(row[i++]));
        waiting_interrupt_digits_ = ANT(row[i++]);
        ACE_DEBUG((LM_DEBUG,"got queue maxlen=%d on_digit_action_while_waiting=%d waiting_interrupt_digits=%s\\n",
            maxlen_, on_digit_action_while_waiting_, waiting_interrupt_digits_.c_str()));
        return true;
        }
    ACE_DEBUG((LM_WARNING,"no such queue\\n"));
    return false;
    }
    '''
    trailor= '''
    Log(QMANS, QMANS_DEBUG, "Loaded {}: %zu, last column: %u \\n", pM{}->size(),col);
    Log(QMANS, QMANS_DEBUG, "   (Updated PMPbxIds_m: %zu)\\n", PMPbxIds_m->size());

    M{}Lock_m.write_lock();
    PM{}_m.swap(pM{});
    M{}Lock_m.unlock();
'''
    ##print(template(variable_template,'{}', 'QueueData'))
    from_QueueMan_i_to_QmanService(variable_template + corba_qman_code + trailor, 'QueueData')

class make_xlat():
    def __init__(self, *args, **kwds):
        self.adict = dict(*args, **kwds)
        self.rx = self.make_rx( )
    def make_rx(self):
        return re.compile('|'.join(map(re.escape, self.adict)))
    def one_xlat(self, match):
        return self.adict[match.group(0)]
    def __call__(self, text):
        return self.rx.sub(self.one_xlat, text)

if __name__ == '__main__':
    main(sys.argv[1:])
