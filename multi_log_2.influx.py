#!/usr/bin/env python

import shlex, subprocess, socket, os, time, signal, sys
from time import sleep
from subprocess import call, Popen, check_output, PIPE
from nbstreamreader import NonBlockingStreamReader as NBSR

log_server = 'xdev64.xcastlabs.com'
def add_dev_log(log ='db'):

    influx_writer='/home/nir/bin/table_2_db.py --chunk=10000'
    logname = "~/logs/{}.log".format(log)
    parser = 'awk -v name={} -f /home/nir/bin/log_2_table.awk'.format(log)
    if('db' == log):
         parser = '/home/nir/bin/db_2_table.awk'
    #elif('mserver' == log):
    #    pass
    elif('conf' == log):
        logname = "~/logs/{}.log".format('hstarter')

    remote_log_cmd ="ssh xcast@{} 'tail -0f {}'".format(log_server,logname)
    return remote_log_cmd,parser,influx_writer

def run(remote_log_cmd,parser,influx_writer, execute_cmd='./dev_conf_2_influxdb.sh'):
    args = shlex.split(remote_log_cmd)
    try:
        p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE,shell=False, bufsize=0)
        awk = Popen(shlex.split(parser), stdin=p.stdout, stdout=PIPE, shell=False, bufsize=0)
        p.stdout.close()    # Allow awk to receive a SIGPIPE if p exits.
        uploader = Popen(shlex.split(influx_writer), stdin=awk.stdout, stdout=PIPE, shell=False, bufsize=0)
        awk.stdout.close()  # Allow uploader to receive a SIGPIPE if awk exits.

    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        print __file__, 'Oops'
        p.kill()
        sys.exit(-1)
    try:
        print check_output(execute_cmd)
        #error = p.stderr.readlines()                 #blocking call, wait until done
        #time.sleep(30)
        p.kill()
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        print __file__, 'Oops'
        p.kill()
        sys.exit(-1)

#(remote_log_cmd,parser,influx_writer) = add_dev_log('mserver')
#(remote_log_cmd,parser,influx_writer) = add_dev_log('db')
#run (remote_log_cmd,parser,influx_writer,'./dev_conf_2_influxdb.sh')
#(remote_log_cmd,parser,influx_writer) = add_dev_log('mserver')
(remote_log_cmd,parser,influx_writer) = add_dev_log('mserver')
run (remote_log_cmd,parser,influx_writer,'./dev_qman_2_influxdb.sh')
'''
print "{} | {} | {}".format(*add_dev_log())
print "{} | {} | {}".format(*add_dev_log('mserver'))
print "{} | {} | {}".format(*add_dev_log('conf'))
print "{} | {} | {}".format(*add_dev_log('db'))
print "{} | {} | {}".format(*add_dev_log('qman'))
print './dev_conf_2_influxdb.sh'
print "{} | {} | {}".format(*add_dev_log('qman'))
print './dev_qman_2_influxdb.sh'
'''
