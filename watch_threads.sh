#!/bin/bash

[[ -z $1 ]] && app_name='./middle_kafka_producer.py' || app_name="$1"
main_process=$(pgrep -f ${app_name})
watch -n 0.3 "ps -LF H -p ${main_process}"

 