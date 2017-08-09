#!/usr/bin/env python

from subprocess import check_output
cmd= '''
    a=`ps -ef | grep -v grep | grep baresip`
    if [ "" = "$a" ] ; then echo run /usr/local/bin/baresip as root
    else
    curl 'http://127.0.0.1:8000/?/auloop'
    for i in `seq 1 30`;do bsTestPrdRPMLoop.sh ; sleep 1; done
    sleep 10;
    echo curl 'http://127.0.0.1:8000/?lTlTlTlTlTlTlT'
    curl 'http://127.0.0.1:8000/?lTlTlTlTlTlTlT'
    fi
'''



print check_output(shlex.split(cmd))    # blocking call, wait until done testPrdRPM.py

