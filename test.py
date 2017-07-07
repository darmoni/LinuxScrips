#!/usr/bin/env python
import shlex, subprocess
import socket
import os
import time
from decimal import *
from time import sleep
from subprocess import call, Popen, check_output, PIPE
from nbstreamreader import NonBlockingStreamReader
from baresip_testing import tester, logger, configure
import signal
import sys, getopt

def safe_exit(level, frame):
    exit(0)

def sig_handler(sig, frame):
    print ("got sig({})\n".format(sig))
    safe_exit(sig, frame)

signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)

def main(argv):

    what_2do = configure().get_parameters(argv)
    if len(what_2do) < 10:
        print '!!!Error!!!','number of fields is worng',len(what_2do)
        exit(0)
    print 'number of fields is correct',len(what_2do)
    '''                                        0----------------1--------------------2--------------------------3------------------------4--------5-----------------------------6----7---------8----9
    'qman_staging_local_logs':['stage1n1-la.siptalk.com','bairsip.xcastlabs.com','staging_bsTestQman.py','stage1n1-la.siptalk.com','/qman.log','/home/nir/bin/qman_events.awk',False,20,'staging','qman'],
    'qman_staging_local_logs':['stage1n1-la.siptalk.com','bairsip.xcastlabs.com','staging_bsTestQman.py','stage1n1-la.siptalk.com','/qman.log',False,20,'staging','qman'],
    'qman_dev':               ['xdev64.xcastlabs.com'   ,'bairsip.xcastlabs.com','dev_bsTestQman.py'    ,'xdev64.xcastlabs.com'   ,'/qman.log',False,40,'dev'    ,'qman']
    '''
    print what_2do
    #exit(0)
    xcast_user = 'xcast'
    user = xcast_user
    (target_server, testserver, COMMAND, logserver, log_name, log_filter, using_logserver, sleep_time, setup, target) = what_2do

    print 'Testing from Server is', testserver
    print  "Starting", (time.strftime("%H:%M:%S"))
    try:
        if(0 == len(logserver)): #('conf' == target):
            #PrintFrame()
            sleep_time =0 # no logs are collected/filtered, so no settling down is needed
            my_tester=tester()
        else:
            path = "~"+xcast_user+"/logs"
            commands = ("tail -0f ",log_name+"\n")

            print __file__,logserver,path,setup,target,using_logserver,commands

            thelogger = logger(target_server,path,setup,target,using_logserver,commands,logserver)
            #PrintFrame()
            params = thelogger.which_server_to_monitor_logs_on()
            #PrintFrame()
            print params #logserver, path
            if(0 == len(log_filter)):
                my_tester=tester(params[0],params[1],'')
            else:
                my_tester=tester(params[0],params[1],log_filter)

        my_tester.test(user,testserver,COMMAND,sleep_time)
        print  "Test ended", (time.strftime("%H:%M:%S"))
        if(0 < len(logserver)):
            count_commands = "ssh "+xcast_user+"@"+logserver +" 'ps -ef | grep "+commands[1].strip()+" | grep -v grep |grep "+xcast_user+"| wc -l'"
            #PrintFrame()
            print count_commands
            #PrintFrame()
            count_loggers = shlex.split(count_commands)
            print 'current logging jobs on server:',check_output(count_loggers)

    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        print __file__, 'Oops'

if __name__ == "__main__":
   main(sys.argv[1:])
