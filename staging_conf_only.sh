#! /bin/bash -x
time=`timestamp | sed 's/[:|-]//g'`;
#date; time test.py -p conf_staging; date
#test.py -p conf_staging_log_server |table_2_db.py
date;time test.py -p conf_staging_log_server_log_only | tee /tmp/conf_staging_log_server_log_only.$time.log |log_2_table.awk | table_2_db.py;date
