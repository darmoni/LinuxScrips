#! /bin/bash
# $Id$ $Date$

mydirname=`dirname $0`
. $mydirname/testRTP.cfg
if [ ! -n "$1" ]; then
calls=56
else
calls=$1
fi
list='';for i in `seq 1 $calls`; do list=$list'lT'; done
curl_cmd=$baresip_access_curl$list
a=`ps -ef | grep -v grep | grep baresip | grep root`
if [ "" = "$a" ] ; then echo run  /usr/local/bin/baresip as root
else
curl $baresip_access_curl'/auloop'
for i in `seq 1 $calls`;do $mydirname/bsTestPrdRTPLoop.sh 2> /dev/null; sleep 1; done
sleep 1;
echo curl $curl_cmd
curl $curl_cmd
fi
