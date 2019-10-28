#!/bin/bash

servers='pbxdev.xcastlabs.com pps.siptalk.com'
if [[ "Prepare" =~ "$*" ]] ; then
    for build_server in ${servers} ; do
        #echo 'Prepare ing'
        echo "Preparing ${build_server}"
        ssh ndarmoni@${build_server} "cd git_rpm_scripts ; make clean_clean"; # less verbose than 'make clean'
    done
elif [[ "Status" =~ "$*" ]] ; then
    for build_server in ${servers} ; do
        echo "Statusing ${build_server}"
        ssh ndarmoni@${build_server} "cd git_rpm_scripts/Registrator ; git sst"
    done
else
    ssh ndarmoni@pbxdev.xcastlabs.com "cd git_rpm_scripts ; ./change_manager.py $*"
fi

exit 0
