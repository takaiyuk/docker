#!/bin/bash
if [ "$1" == "" ]; then
  sudo docker build . -t takaiyuk/ml-table -f ./Dockerfile
else
  sudo docker build . -t $1 -f ./Dockerfile
fi
