#!/usr/bin/bash

check_cores.sh 2> /dev/null | sort -u | grep -v container | core_name.py | sort -u | grep -v errors.log
#check_cores.sh 2> /dev/null | grep core | sort -u | ~/bin/core_name.py | sort -u | grep -v errors.log | egrep 'container[[:digit:]]+-la.xcastlabs.net|[[:alpha:]]+-pbxsm-production-'
