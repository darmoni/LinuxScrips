#! /bin/bash
a=`ps -ef | grep -v grep | grep baresip | grep root`
if [ "" = "$a" ] ; then echo nothing to do, baresip is not running
else 
curl 'http://127.0.0.1:33000/?q'
fi
