#! /bin/bash
mydirname=`dirname $0`
. $mydirname/testRTP.cfg
#echo "'$mydirname' , '$baresip_access_curl'"
curl $baresip_access_curl'd2244563400' > /dev/null
