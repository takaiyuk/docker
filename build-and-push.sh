#!/bin/bash
if [ "$1" == "" ] || [ "$2" == "" ]; then
  echo arguments must not be empty
  exit 1
else
  cd $1 && cd $2 && ./build.sh && ./push.sh && cd ../..
fi
