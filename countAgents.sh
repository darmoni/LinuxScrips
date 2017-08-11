#! /bin/bash
mydirname=`dirname $0`
. $mydirname/testRTP.cfg

curl $baresip_access_curl'r' 2> /dev/null | awk '/--- Useragents: / { print $3}'
