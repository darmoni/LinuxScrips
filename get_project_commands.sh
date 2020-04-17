#!/bin/bash

servers='pbxdev.xcastlabs.com'
if [[ "Prepare" =~ "$*" ]] ; then
    for build_server in ${servers} ; do
        #echo 'Prepare ing'
        echo "
        Preparing ${build_server}
        "
        # less verbose than 'make clean'
        ssh ndarmoni@${build_server} "cd git_rpm_scripts ; make clean_clean"
    done
elif [[ "RepoPrepare" =~ "$*" ]] ; then
    for build_server in ${servers} ; do
        echo "
        Repo Preparing ${build_server}
        "
        ssh ndarmoni@${build_server} "cd google_repo_rpm/.repo/manifests && make all"
    done
elif [[ "Status" =~ "$*" ]] ; then
    for build_server in ${servers} ; do
        echo "
        Statusing ${build_server}
        "
        ssh ndarmoni@${build_server} "cd git_rpm_scripts/Registrator ; git sst"
    done
elif [[ "RepoStatus" =~ "$*" ]] ; then
    for build_server in ${servers} ; do
        echo "
        Repo Statusing ${build_server}
        "
        ssh ndarmoni@${build_server} "cd google_repo_rpm/.repo/manifests && make status"
    done
else
    ssh ndarmoni@pbxdev.xcastlabs.com "cd git_rpm_scripts ; ./change_manager.py $*"
fi

exit 0
