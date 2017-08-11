#! /bin/bash
. ~/bin/testRTP.cfg
if [ ! -n "$1" ]; then
calls=56
else
calls=$1
fi

loops=`echo "(6+$calls)/7" |bc`
list='';for i in `seq 1 $calls`; do list=$list'lT'; done
curl_cmd=$baresip_access_curl$list

list='';for i in `seq 1 7`; do list=$list'bT'; done
curl_bye_cmd=$baresip_access_curl$list

a=`ps -ef | grep -v grep | grep baresip | grep root`
if [ "" = "$a" ] ; then echo nothing to do, baresip is not running
else 
curl $curl_cmd 2> /dev/null
for i in `seq 1 $loops`;do curl $curl_bye_cmd ; sleep 1; done
sleep 1;
curl $curl_cmd 2> /dev/null
fi
