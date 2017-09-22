#! /usr/bin/bash
grep gtt- build*sh | awk -F":PACKAGE_NAME=" '/PACKAGE_NAME=/ {print $2 ":" $1;}' | sort |uniq
