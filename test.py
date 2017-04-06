#!/usr/bin/env python
import shlex, subprocess
import socket
import os
import time
from time import sleep
from subprocess import call, Popen, check_output, PIPE
from nbstreamreader import NonBlockingStreamReader,UnexpectedEndOfStream
from baresip_testing import baresip_test, baresip_test_with_logs
import signal
import sys, getopt

def safe_exit(level):
    exit(0)

def sig_handler(sig, frame):
    print "got sig(", sig,")\n"
    safe_exit(sig)

signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)

def which_server_to_monitor_logs_on(setup,target,server,path):
    if 'dev' == setup:
        logserver = server
    if 'qman' == target and 'staging' == setup:
        logserver = 'logserver3-la.siptalk.com'
        path += '/servers/'+server+'/'+time.strftime("%Y%m%d")
    return (logserver,path)

def main(argv):

    dev_testserver = 'xdev64.xcastlabs.com'
    testserver = 'bairsip.xcastlabs.com'
    logserver = 'stage1n1-la.siptalk.com'
    xcast_user = 'xcast'
    user = 'nir'
    setup = 'staging'
    target = 'qman'
    sleep_time = 20
    using_logserver= False
    COMMAND='bin/bsTestQman.py'
    setups ={'dev':[testserver,dev_testserver,xcast_user,40], setup:[testserver,logserver,user,sleep_time]}
    targets ={target:[COMMAND,],'conf':['bin/bsTestConf.py',]}
    try:
      opts, args = getopt.getopt(argv,"hls:t:",["setup=","target="])
    except getopt.GetoptError:
      print __file__, ' -s <setup> -t <target>'
      exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print __file__, ' -s <setup> -t <target>'
            print 'For Dev Testing:', __file__, '-s dev'
            print 'For Staging Testing:', __file__, '-s staging'
            print 'For Qman Testing:', __file__, '-t qman'
            print 'For Conference Testing:', __file__, '-t conf'
            exit()
        if opt == '-l':
            using_logserver = True
            break
        elif opt in ("-t", "--target"):
            target = arg
            if(target == 'conf'):
                setup = 'staging'
                user = xcast_user
                testserver = setups[setup][0]
                logserver = ''
                sleep_time = setups[setup][3]
                break
            #logserver = targets[target][1]
            #user = targets[target][2]
            #sleep_time = targets[target][3]
        elif opt in ("-s", "--setup"):
            setup = arg
            testserver = setups[setup][0]
            logserver = setups[setup][1]
            user = setups[setup][2]
            sleep_time = setups[setup][3]

    COMMAND=targets[target][0]
    print 'Testing from Server is', testserver

    if(0 < len(logserver)):
        logfile_path = "~/logs"
        #print 'before Log file is:', logserver,logfile_path
        if('staging' == setup and using_logserver): (logserver,logfile_path) = which_server_to_monitor_logs_on(setup,target,logserver,logfile_path)
        #print 'after Log file is:', logserver,logfile_path
        #list_logfiles = shlex.split("ssh "+xcast_user+"@"+logserver +" ls -l "+logfile_path+'/')
        #print 'is this correct? ',check_output(list_logfiles)

    #exit(0)
    print  "Starting", (time.strftime("%H:%M:%S"))
    if(('qman' == target)):
        count_loggers = shlex.split("ssh "+xcast_user+"@"+logserver +" 'ps -ef|grep qman.log|grep -v grep|grep "+xcast_user+"|wc -l'")
        print 'current logging jobs on server:',check_output(count_loggers)
    print setup, target
    #exit(0)
    try:
        if('conf' == target):
            sleep_time =0; # no logs are collected/filtered, so no settling down is needed
            test=baresip_test()
        elif('qman' == target):
            test=baresip_test_with_logs(logserver,"tail -f "+logfile_path+"/qman.log\n",'/home/nir/bin/qman_events.awk')

        test.test(user,testserver,COMMAND,sleep_time)
        #test.test(user,testserver,'ls -ltr',0)

        print 'current logging jobs on server:',check_output(count_loggers)
    except:
        print 'Oops'

if __name__ == "__main__":
   main(sys.argv[1:])
