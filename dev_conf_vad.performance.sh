#!/bin/bash -x
domain="xcastlabs.com"
server=xdev64.$domain
if [ 'YES' == $(ssh xcast@$server 'cat lib/mserver/media.xml' | awk '/AudioProcessing/ {if( $2 ~ /apply="1"/ ) print "YES"; else print "NO";}') ]
then dev_conf_vad.on.performance.sh
else dev_conf_vad.off.performance.sh
fi

#echo '
#dev_conf_vad.on.performance.sh
#else
#dev_conf_vad.off.performance.sh
#fi
