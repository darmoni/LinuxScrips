#!/usr/bin/env python

import sys
from time import sleep
from subprocess import check_output
from collect_logs import log_collector

try:
    #dev_mserver_log_collector=log_collector('mserver')
    #production_qman_log_collector=log_collector('qman','tswitch3.siptalk.com')
    #production_qman_log_collector.run('sleep 50')

    db_log_collector=log_collector('db',"stage1n1-la.siptalk.com",True)
    #dev_db_log_collector=log_collector('db')
    db_log_collector.collect_log()

    #dev_mserver_log_collector=log_collector('mserver',"mserver1n1-la.siptalk.com",True)
    mserver_log_collector=log_collector('mserver',"mserver1n1-la.siptalk.com")
    mserver_log_collector.collect_log()
    conf_log_collector=log_collector('conf',"mserver1n1-la.siptalk.com",True)
    p = conf_log_collector.collect_log()  #.run('/home/nir/bin/staging_qman_2_influxdb.sh')
    check_output('/home/nir/bin/staging_qman_2_influxdb.sh')

    #dev_qman_log_collector=log_collector('qman')
    #dev_qman_log_collector.run('test.py -p qman_dev')#('time sleep {}'.format(60*60))#('time sleeper.sh 120')('./dev_qman_2_influxdb.sh')

    sleep(30)
    p.kill()
    del conf_log_collector
    del mserver_log_collector
    del db_log_collector
    sleep(30)

    #(remote_log_srv_cmd,log_srv_cmd,parser,influx_writer) = add_local_log('mserver')
    #(remote_log_srv_cmd,log_srv_cmd,parser,influx_writer) = add_local_log('db')
    #run (remote_log_srv_cmd,log_srv_cmd,parser,influx_writer,'./dev_conf_2_influxdb.sh')
    #(remote_log_srv_cmd,log_srv_cmd,parser,influx_writer) = add_local_log('mserver')
    #print "{} '{}' | {} | {}".format(remote_log_srv_cmd,log_srv_cmd,parser,influx_writer)
    #run (remote_log_srv_cmd,log_srv_cmd,parser,influx_writer,'./dev_qman_2_influxdb.sh')

    '''
    print "{} '{}' | {} | {}".format(*add_local_log())
    print "{} '{}' | {} | {}".format(*add_local_log('mserver'))
    print "{} '{}' | {} | {}".format(*add_local_log('conf'))
    print "{} '{}' | {} | {}".format(*add_local_log('db'))
    print "{} '{}' | {} | {}".format(*add_local_log('qman'))
    print './dev_conf_2_influxdb.sh'
    print "{} '{}' | {} | {}".format(*add_local_log('qman'))
    print './dev_qman_2_influxdb.sh'
    '''
    sys.exit(0)

except Exception as inst:
    print type(inst)
    print inst.args
    print inst
    print __file__, 'Oops'

