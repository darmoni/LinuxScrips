#!/bin/bash -x
test_server="from_log"
test_mode="mode.unknown"
if [ "" != "$2" ]; then test_server=$test_server."on_$1" ; test_mode="$2" ;
else if [ "" != "$1" ]; then test_server=$test_server."on_$1" ; fi
fi
date
#echo $test_server, $test_mode
hstarter_PacketLossReport_2_table.awk | hstarter_ReportPerfomance_2_table_2_db.py --test_server=$test_server --test_mode=$test_mode;date
