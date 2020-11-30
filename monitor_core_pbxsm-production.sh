#!/usr/bin/bash

ssh nir@10.10.10.55 'cd bin; ./get_project_commands.sh MonitorCores'
#check_cores.sh 2> /dev/null | sort -u | grep -v container | core_name.py | grep -v errors.log  | egrep 'container[[:digit:]]+-la.xcastlabs.net|[[:alpha:]]+-pbxsm-production-'
#check_cores.sh 2> /dev/null | sort -u | grep -v container | core_name.py | sort -u | grep -v errors.log
#check_cores.sh 2> /dev/null | grep core | sort -u | ~/bin/core_name.py | sort -u | grep -v errors.log | egrep 'container[[:digit:]]+-la.xcastlabs.net|[[:alpha:]]+-pbxsm-production-'
