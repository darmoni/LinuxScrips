#! /bin/bash -x
date; time test.py -p conf_staging_log_server_log_only | log_2_table.awk |table_2_db.py ; date
#test.py -p conf_staging_log_server |table_2_db.py
#date;time test.py -p conf_staging_log_server_log_only |tee /tmp/conf_staging_log_server_log_only.log |log_2_table.awk | table_2_db.py;date
