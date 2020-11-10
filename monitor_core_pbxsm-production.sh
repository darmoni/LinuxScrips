#!/usr/bin/bash

check_cores.sh 2> /dev/null | grep core | sort -u | awk -f ~/bin/core_name.awk | sort -u | grep -v errors.log | egrep 'container[[:digit:]]+-la.xcastlabs.net|[[:alpha:]]+-pbxsm-production-'
