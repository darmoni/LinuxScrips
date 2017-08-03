#! /bin/bash -x
time=`timestamp | sed 's/[:|-]//g'`;
date;time test.py -p conf_dev_local_logs_log_only | hstarter_ReportPerfomance_2_table.awk | hstarter_ReportPerfomance_2_table_2_db.py --test_server=dev --test_mode=vad.on;date
