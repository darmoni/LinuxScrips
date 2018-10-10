#!/bin/bash

if [[ "Prepare" =~ "$*" ]] ; then
    #echo 'Prepare ing'
    ssh ndarmoni@pbxdev.xcastlabs.com "cd git_rpm_scripts ; make clean"
elif [[ "Status" =~ "$*" ]] ; then
    #echo ' Status ing'
    ssh ndarmoni@pbxdev.xcastlabs.com "cd git_rpm_scripts/Registrator ; git sst"
else
    ssh ndarmoni@pbxdev.xcastlabs.com "cd git_rpm_scripts ; ./change_manager.py $*"
fi

exit 0
