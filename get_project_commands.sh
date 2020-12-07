#!/bin/bash

TZ="America/Chicago"

#servers='voicedev1.xcastlabs.net pbxdev.xcastlabs.com'
timestamp=$(date)
servers='voicedev1.xcastlabs.net'
if [[ "Prepare" =~ "$*" ]] ; then
    for build_server in ${servers} ; do
        #echo 'Prepare ing'
        echo " ${timestamp}
        Preparing ${build_server}
        "
        # less verbose than 'make clean'
        ssh ndarmoni@${build_server} "cd ~/git_rpm_scripts && make clean_clean"
    done
elif [[ "RepoPrepare" =~ "$*" ]] ; then
    for build_server in ${servers} ; do
        echo " ${timestamp}
        Repo Preparing ${build_server}
        "
        ssh ndarmoni@${build_server} "cd ~/repo_rpm_projects/.repo/manifests  && make all && git diff"
    done
elif [[ "Status" =~ "$*" ]] ; then
    for build_server in ${servers} ; do
        echo " ${timestamp}
        Statusing ${build_server}
        "
        ssh ndarmoni@${build_server} "cd ~/git_rpm_scripts && cd Registrator ; git sst"
    done
elif [[ "RepoStatus" =~ "$*" ]] ; then
    for build_server in ${servers} ; do
        echo " ${timestamp}
        Repo Statusing ${build_server}
        "
        ssh ndarmoni@${build_server} "cd ~/repo_rpm_projects/.repo/manifests  && make status"
    done
elif [[ "MonitorCores" =~ "$*" ]] ; then
    for build_server in ${servers} ; do
        echo " ${timestamp}
        Checking SM cores using ${build_server}
        "
        ssh ndarmoni@${build_server} "cd ~/bin; ./monitor_core_pbxsm-production.sh"
    done
else
    for build_server in ${servers} ; do
        ssh ndarmoni@${build_server}  "cd git_rpm_scripts ; ./change_manager.py $*"
    done
fi
exit 0
