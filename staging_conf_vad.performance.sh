#!/bin/bash -x
server='stage1n1-la.siptalk.com'
if [ 'YES' == $(ssh xcast@$server 'cat lib/mserver/media.xml' | awk '/AudioProcessing/ {if( $2 ~ /apply="1"/ ) print "YES"; else print "NO";}') ] ;
then staging_conf_vad.on.performance.sh;
else staging_conf_vad.off.performance.sh;
fi
