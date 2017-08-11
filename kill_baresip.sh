#! /bin/bash
mydirname=`dirname $0`
. $mydirname/testRTP.cfg

a=`ps -ef | egrep -v 'grep|ssh' | grep -v $$ | grep "/usr/local/bin/baresip" |grep root | awk '! /sudo/{print $2;}'`

if [ "" = "$a" ] ; then echo nothing to do, baresip is not running

else 
echo I am "$$" found these "$a" candidates
for b in $a;
do if [ "$$" != "$b" ] ; then echo killing $b;
        echo `ps -ef | egrep -v 'grep|ssh' | grep -v $$ | grep $b`;
        $(kill $b); sleep 1 ;
        fi;
done
curl $baresip_access_curl'q'
sleep 1
echo `ps -ef | egrep -v 'grep|ssh' | grep -v $$ | grep "/usr/local/bin/baresip" |grep root | awk '! /sudo/'`
fi
