#!/usr/bin/env python
'''
import shlex, subprocess, socket, os, time, signal, sys, datetime
from time import sleep
from subprocess import call, Popen, check_output, PIPE
from nbstreamreader import NonBlockingStreamReader as NBSR

class log_collector:
    def __init__(self, log ='db', log_server = 'xdev64.xcastlabs.com', syslog=False):
        self._server=log_server
        self._log=log
        self._p = -1
        if syslog:self._params =self.add_syslog_log(self._log,self._server)
        else :self._params =self.add_local_log(self._log,self._server)

    def collect_log(self):
        (remote_log_srv_cmd,log_srv_cmd,parser,influx_writer) = self._params
        self.setup()
        if(-1 != self._p):
            self._p.stdin.write(log_srv_cmd)
            return self._p

    def add_local_log(self, log, log_server):

        influx_writer='/home/nir/bin/table_2_db.py'
        logname = "~/logs/{}.log".format(log)
        parser = 'awk -v name={} -f /home/nir/bin/log_2_table.awk'.format(log)
        if('db' == log):
             parser = '/home/nir/bin/db_2_table.awk'
        elif('qman' == log):
            parser = '/home/nir/bin/qman_2_table.awk'
        elif('conf' == log):
            logname = "~/logs/{}.log".format('hstarter')

        remote_log_srv_cmd ="ssh xcast@{}".format(log_server)
        log_srv_cmd ="tail -0f {}\n".format(logname)
        return remote_log_srv_cmd,log_srv_cmd,parser,influx_writer

    def add_syslog_log(self, log, log_source, log_server = "logserver3-la.siptalk.com"):

        influx_writer='/home/nir/bin/table_2_db.py'
        logname = "~/logs/servers/{}/{}/{}.log".format(log_source, datetime.datetime.today().strftime("%Y%m%d"),log)
        parser = 'awk -v name={} -f /home/nir/bin/log_2_table.awk'.format(log)
        if('db' == log):
             parser = '/home/nir/bin/db_2_table.awk'
        elif('qman' == log):
            parser = '/home/nir/bin/qman_2_table.awk'
        elif('conf' == log):
            logname = "~/logs/servers/{}/{}/{}.log".format(log_source, datetime.datetime.today().strftime("%Y%m%d"),'hstarter')

        remote_log_srv_cmd ="ssh xcast@{}".format(log_server)
        log_srv_cmd ="tail -0f {}\n".format(logname)
        return remote_log_srv_cmd,log_srv_cmd,parser,influx_writer

    def setup(self):
        (remote_log_srv_cmd,log_srv_cmd,parser,influx_writer) = self._params
        print "{} '{}' | {} | {}".format(remote_log_srv_cmd,log_srv_cmd,parser,influx_writer)
        #return
        args = shlex.split(remote_log_srv_cmd)
        try:
            p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE,shell=False, bufsize=0)
            awk = Popen(shlex.split(parser), stdin=p.stdout, stdout=PIPE,stderr=PIPE, shell=False, bufsize=0)
            p.stdout.close()    # Allow awk to receive a SIGPIPE if p exits.
            uploader = Popen(shlex.split(influx_writer), stdin=awk.stdout, stdout=PIPE,stderr=PIPE, shell=False, bufsize=0)
            awk.stdout.close()  # Allow uploader to receive a SIGPIPE if awk exits.
            print "DEBUG. Made it through setup of log parsing"
            self._p = p
        except Exception as inst:
            self._p = -1
            print type(inst)
            print inst.args
            print inst
            print __file__, 'Oops'
            p.kill()
            sys.exit(-1)

    def run(self, execute_cmd='/home/nir/bin/dev_conf_2_influxdb.sh'):
        (remote_log_srv_cmd,log_srv_cmd,parser,influx_writer) = self._params
        self.setup()
        try:
            if(-1 == self._p): return
            p = self._p
            p.stdin.write(log_srv_cmd)                      # start logging
            print "DEBUG. Strated logging. will run '%s' now..." % execute_cmd
            print check_output(shlex.split(execute_cmd))    # blocking call, wait until done
            #error = p.stderr.readlines()                   # blocking call, wait until done
            #time.sleep(30)
            self._p = -1
            p.kill()
        except Exception as inst:
            self._p = -1
            print type(inst)
            print inst.args
            print inst
            print __file__, 'Oops'
            p.kill()
            sys.exit(-1)
'''
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
    conf_log_collector.run('./staging_conf_only.sh')
    #check_output('/home/nir/bin/staging_conf_only.sh')

    #dev_qman_log_collector=log_collector('qman')
    #dev_qman_log_collector.run('test.py -p qman_dev')#('time sleep {}'.format(60*60))#('time sleeper.sh 120')('./dev_qman_2_influxdb.sh')

    sleep(30)

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