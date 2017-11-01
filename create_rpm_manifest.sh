#!/usr/bin/env bash
mydirname=$(dirname $(realpath $0))
dd=$1
manifest_name=$2
cd Registrator/$dd &&
  echo "Entering 'Registrator/$dd'" >> $manifest_name &&
  $mydirname/record_repo.sh >> $manifest_name &&
cd $mydirname
