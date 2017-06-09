from weakref import WeakValueDictionary
import signal

def sig_handler(sig, frame):
    print "got sig({})\n".format(sig)
    safe_exit(sig)

signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)

def safe_exit(level):
    # save stuff
    print("Exiting ...\n")
    exit(0)

class Counter:
    _instances = WeakValueDictionary()
    @property
    def Count(self):
        return len(self._instances)

    def __init__(self, name):
        self.name = name
        self._instances[id(self)] = self
        print 'created'

    def __del__(self):
        print 'deleted'
        if self.Count == 0:
            print 'Last Counter object deleted'
        else:
            print self.Count, 'Counter objects remaining'

#!/usr/bin/env python

from time import sleep
from subprocess import check_output
from collect_logs import log_collector

try:
    dev_hstarter_log_collector=Counter(log_collector('conf'))
    dev_db_log_collector=Counter(log_collector('db'))
    #dev_mserver_log_collector=Counter(log_collector('mserver',execute_cmd ='dev_qman_2_influxdb.sh'))
    dev_mserver_log_collector=Counter(log_collector('mserver'))
    for id in Counter._instances:
        Counter._instances[id].name.execute()
    sleep (5*60)
    #dev_db_log_collector.execute()
    #dev_mserver_log_collector.execute()
    #del dev_mserver_log_collector
    #del dev_db_log_collector
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

except Exception as inst:
    print type(inst)
    print inst.args
    print inst
    print __file__, 'Oops'

