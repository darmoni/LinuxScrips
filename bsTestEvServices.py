#!/usr/bin/env python
import shlex, subprocess
import socket
import os
import time
from time import sleep
from subprocess import call, Popen, check_output, PIPE
from nbstreamreader import NonBlockingStreamReader as NBSR

def make_calls (cmdline,count,agents,dial):
    print "cycling(count)\n"
    for i in range(count):
        who = dial[i % len(dial)]
        call = "d"+who+"\n"
        print call
        cmdline.write(call)
        sleep (0.1)
        cmdline.write("T")

def test_event_server (cmdline,count,agents,dial):
    print "cycling(count)\n"
    for i in range(count):
        who = dial[i % len(dial)]
        cmdline.write("b")
        sleep (0.1)
        call = "d"+who+"\n"
        print call
        cmdline.write(call)
        sleep (3)
        cmdline.write("T")

def safe_exit(level):
    global cmdline
    global calls
    global process
    # save stuff
    print("Exiting ...\n")
    cleanup(calls, cmdline)
    exit(0)

def sig_handler(sig):
    print "got sig(sig)\n"
    safe_exit(sig)

#pcntl_signal(SIGINT,  "sig_handler")
#pcntl_signal(SIGTERM, "sig_handler")
#pcntl_signal(SIGHUP,  "sig_handler")

def cleanup (calls, cmdline):
    global agents

#    if(is_numeric(calls)):
    print "Number of calls to close is " , calls, "\n"
    for a_calls in range(calls):
        cmdline.write("b")
        sleep(0.01)
        if(1 < agents):
            cmdline.write('T\n')

TIMEOUT_SECONDS = 2*60

def testing(count, agents, dial):
    global cmdline

    make_calls(cmdline,count,agents,dial)
    timeout = time.time()
    timeoutStarted = True
    while (True):
        test_event_server(cmdline,count,agents,dial)
        if (time.time() > (timeout + TIMEOUT_SECONDS)):
            print "timeout\n"
            cleanup(count,cmdline)
            break
'''        
            while (false !== ($line = fgets(STDIN))) {
                echo $line;
                if('q' == $line[0]) {
                    $calls = intval(substr($line,1));
                    if(is_numeric($calls)){
                        if (0 == $calls) $calls = $count;
                        echo "Number of calls to close is $calls\n";
                        $break = true;
                    }
                }
                else
                    fwrite($cmdline, rtrim($line));
                if ($timeoutStarted) {
                    $timeoutStarted = false;
                    $timeout = null;
                }
            }
            if($break) {
                cleanup($count,$cmdline);
                break;
            }
            if (feof(STDIN)) {
                echo "feof\n";
                break;
            }

            $status = proc_get_status($process);
            // check retval
            if ($status === FALSE) {
                throw new Exception("Failed to obtain status information for $pid");
            }
            if ($status['running'] === FALSE) {
                $exitcode = $status['exitcode'];
                $pid = -1;
                echo "Process exited with code: $exitcode\n";
                fclose($cmdline);

                // It is important that you close any pipes before calling
                // proc_close in order to avoid a deadlock
                $return_value = proc_close($process);

                echo "command returned $return_value\n";
                exit($exitcode);
            }
            

#calls = 512
#calls = 256
calls = 128
print "dialing - calls\n"
dial = array("55560", "3000", "3001", "70062", "4703","67892","4701","713300")
agents = 5

print_r(dial)
// echo "cat /tmp/error-output.txt\n";
testing(calls, dial, agents);
'''

calls = 4
print "dialing - ", calls, "calls\n"
dials = ("55560", "3000", "3001", "70062", "4703","67892","4701","713300")
#dials = ("8600",)
agents = 2;
#agents = 1;
print dials
port = '5565'
#port = '5555'
args = shlex.split('/bin/netcat -u 127.0.0.1 ' + port)
p = Popen(args, stdin=PIPE, stdout=PIPE,stderr=PIPE, shell=False)
nbsr = NBSR(p.stdout)
cmdline=p.stdin

'''
cmdline.write("rlTlT\n")
while True:
    output = nbsr.readline(0.9)
    # 0.1 secs to let the shell output the result
    if not output:
        print '[No more data]'
        break
    print output

for call in dials:
    call = 'd'+call+"\n"
    print call
    cmdline.write(call)
# get the output
    while True:
        output = nbsr.readline(0.1)
        # 0.1 secs to let the shell output the result
        if not output:
            print '[No more data]'
            break
        print output
'''
testing(calls,agents,dials)
sleep(10)
cleanup(calls,cmdline)
