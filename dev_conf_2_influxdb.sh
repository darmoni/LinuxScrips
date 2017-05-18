#! /bin/bash -x
time test.py -p conf_dev_local_logs_log_only | log_2_table.awk |table_2_db.py
