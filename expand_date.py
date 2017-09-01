#! /usr/bin/env python
# $Id$ $Date$

import shlex, sys
from subprocess import check_output

data = sys.stdin.read()
args = shlex.split('git log --pretty=format:"%ad" -1')
last_date = check_output(args)
print data.replace('$Date$', '$Date: ' + last_date + '$')
