#! /bin/bash -x
time test.py -p qman_staging_log_server_log_only | qman_2_table.awk |table_2_db.py
