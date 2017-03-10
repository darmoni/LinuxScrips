#!/usr/bin/env python
import shlex, subprocess
import socket
import os
import time
from time import sleep
from subprocess import call, Popen, check_output, PIPE
from nbstreamreader import NonBlockingStreamReader as NBSR
import signal



#logs = 
'''
13:52:03.181926|
13:52:21.171499|handle_timeout start (action_counter,progress_counter,size(_queue_records)=(0, 0, 0)
13:52:42.422399|agent_create_by_account_id_for_login(8064)
13:52:42.422501|select count(agent_id) as counter from agent_assignment where agent_id = 8064;
13:52:42.424349|QueueMan_i.cpp 2988 ...
13:52:42.424414|select agent_data.account_id,agent_data.parent_id,agent_data.phone_number,agent_data.hard_login_time, agent_data.soft_login_time, agent_data.hard_logoff_time,agent_data.soft_logoff_time, agent_data.unanswered_calls_limit, agent_data.unanswered_calls_cnt,agent_data.next_call_can_start, agent_data.last_call_end_time,agent_data.calls_served, agent_data.is_queue_supervisor, agent_data.call_status, account.phonePassword from agent_data left join account on account.id = agent_data.account_id where account.id=8064;
13:52:42.425314|got VALID agent account_id 8064 takeInUse TakeInUse_No
13:52:42.425349|init agent 8064
13:52:42.425383|select a.id from account a, inbound i where i.accountId=a.id and a.isDeleted=0 and a.type=1 and i.phone = '7065S01' and a.parentId = 7747;
13:52:42.426477|phone account id for '7065S01@xcaststaging.voippbxsite.net' was found as 8066
13:52:42.426517|init agent 8064 call_status_='AV' permanent_=0 logged_in_=0
13:52:42.426589|XCastAgrSender::send snding event 0,8064,7747 [IU]
13:52:42.426823|QueueMan_i.cpp 2971 ...
13:52:49.598705|schedule_hard_logoff(8064)
13:52:49.598825|update agent_data set phone_number = '',hard_login_time = 1489171969, soft_login_time = 0, hard_logoff_time = 0,soft_logoff_time = 0, unanswered_calls_cnt = 0,next_call_can_start = 0, last_call_end_time = 0,calls_served = 0, call_status = 'NA', login_status = 0 where account_id = 8064;
13:52:49.604974|XCastAgrSender::send snding event 0,8964,7747 [NA]
13:52:49.605058|insert into agent_records (account_id,ts,end_state, from_phone, reason) values (8064,1489171969,'NA','7065S01@xcaststaging.voippbxsite.net', 'schedule_hard_logoff');
13:52:52.181689|end_of_login(8064)
13:52:52.181775|deactivate_object <agent8064>
13:52:52.181818|reconsider agent 8064 changed state
13:52:52.181839|select queue_id from agent_assignment where agent_id = 8064 order by rand();
13:52:52.183814|reconsider queue 28177 with agent account 8064
13:52:52.183852|active queues size 0 queue_id = 28177
13:52:52.183867|reconsider queue 51626 with agent account 8064
13:52:52.183879|active queues size 0 queue_id = 51626
13:52:52.183890|reconsider queue 8036 with agent account 8064
13:52:52.183902|active queues size 0 queue_id = 8036
13:52:52.183913|reconsider queue 13613 with agent account 8064
13:52:52.183924|active queues size 0 queue_id = 13613
'''

def read_results(results):
    while True:
      try:
        line =results.readline() 
        if(None == line):
            break
        print line,
      except:
        break


def copy_results(results, output):
    print 'copy_results(results, output)\n'
    while True:
      try:
        line =results.readline() 
        if(None == line):
            break
        output.stdin.write(line+"\n")
      except:
        break

def safe_exit(level):
    global p
    read_results(p)
    exit(0)

def sig_handler(sig, frame):
    print "got sig(", sig,")\n"
    safe_exit(sig)

signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)

# examples
'''
p1 = Popen(shlex.split('cat qman.log.sample'), stdout=PIPE)
p2 = Popen(shlex.split('/home/nir/bin/qman_events.awk'), stdin=p1.stdout, stdout=PIPE)
p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
output = p2.communicate()[0]
print output,

p1 = Popen(["dmesg"], stdout=PIPE)
p2 = Popen(["grep", "hda"], stdin=p1.stdout, stdout=PIPE)
p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
output = p2.communicate()[0]
print output,
#
'''
try:
#    args = shlex.split('cat qman.log.sample')
    args = shlex.split('ssh xcast@stage1n1-la.siptalk.com')    
    server = Popen(args,stdin=PIPE,stdout=PIPE,stderr=PIPE, shell=False)
except:
    print 'could not connect to servers 1'
    exit(-1)
p = server
events= NBSR(p.stdout)

server.stdin.write("tail -f ~xcast/logs/qman.log\n")

try:
    args = shlex.split('/home/nir/bin/qman_events.awk')
    events_filter = Popen(args, stdin=PIPE, stdout=PIPE,stderr=PIPE, shell=False)
except:
    print 'could not connect to servers 2'
    exit(-1)



#results = NBSR(events_filter.stdout)

#sleep(20)
import subprocess
import sys

HOST="nir@bairsip.xcastlabs.com"
# Ports are handled in ~/.ssh/config since we use OpenSSH
COMMAND="bin/bsTestQman.py"

ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
result = ssh.stdout.readlines()
if result == []:
    error = ssh.stderr.readlines()
    print >>sys.stderr, "ERROR: %s" % error
#else:
    #print result

#read_results(events) 

copy_results(events,events_filter)
print events_filter.communicate()[0]
