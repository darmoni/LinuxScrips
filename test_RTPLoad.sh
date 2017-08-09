#! /bin/bash
if [ ! -n "$1" ]; then
calls=56
else
calls=$1
fi
curl_cmd='http://127.0.0.1:33000/?lTlTlTlTlTlTlT'
a=`ps -ef | grep -v grep | grep baresip | grep root`
if [ "" = "$a" ] ; then echo run  /usr/local/bin/baresip as root
else
curl 'http://127.0.0.1:33000/?/auloop'
for i in `seq 1 $calls`;do ~/bin/bsTestPrdRPMLoop.sh ; sleep 1; done
sleep 1;
echo curl $curl_cmd
curl $curl_cmd
fi
