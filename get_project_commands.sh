#!/bin/bash

ssh ndarmoni@pbxdev.xcastlabs.com "cd git_rpm_scripts ; ./change_manager.py -p $1"
exit 0
