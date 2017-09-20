#! /bin/bash -x
if [ -z $1 ] ; then echo "Usage: $0 <production log file>"
else
time=`timestamp | sed 's/[:|-]//g'`;
date;time cat $1 | hstarter_ReportPerfomance_2_table.awk | hstarter_ReportPerfomance_2_table_2_db.py --test_server=prd --test_mode=vad.on;date
fi
