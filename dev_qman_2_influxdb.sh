#! /bin/bash -x
time test.py -p qman_dev_local_logs_log_only | qman_2_table.awk |table_2_db.py
