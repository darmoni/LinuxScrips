#!/bin/bash

unset TS

if [ -z "$*" ]; then
    TS=`date +%s`
else
   echo  "$*" | egrep -q '[^0-9]'
    if [ $? -eq 0 ];then
	TS=`date +%s -d "$*" 2>/dev/null`
    else
	TS=$*
    fi
fi 

LTM=`date -d "1970-01-01 UTC $TS sec" 2>/dev/null`
if [ $? -ne 0  -o  -z "$TS" ]; then
    echo Incorrect date: $*
    exit 1
fi

UTM=`date -u "+%Y-%m-%d %H:%M:%S UTC" -d "1970-01-01 UTC $TS sec"`

echo -e $TS '  ===>  ' $LTM '  ===>  ' $UTM
