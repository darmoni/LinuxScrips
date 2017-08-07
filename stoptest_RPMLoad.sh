#! /bin/bash
if [ ! -n "$1" ]; then
calls=56
else
calls=$1
fi

loops=`echo "(6+$calls)/7" |bc`
curl_cmd='http://127.0.0.1:33000/?lTlTlTlTlTlTlT'
curl_bye_cmd='http://127.0.0.1:33000/?bTbTbTbTbTbTbT'
a=`ps -ef | grep -v grep | grep baresip | grep root`
if [ "" = "$a" ] ; then echo nothing to do, baresip is not running
else 
curl $curl_cmd
for i in `seq 1 $loops`;do curl $curl_bye_cmd ; sleep 1; done
sleep 1;
curl $curl_cmd
fi
