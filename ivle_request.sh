#!/bin/bash

usage() { printf "Usage: [-d <duration in days, int>] [-m <space separated string of modules>]\n"; exit 0;}

[ $# -eq 0 ] && usage 

while getopts ":d:m:" arg; do 
  case $arg in 
    d)
      DURATION=${OPTARG}
      ;;
    m)
      MODULES=${OPTARG}
      ;;
  esac
done

python3 ivle_request.py -d $DURATION -m ${MODULES}
