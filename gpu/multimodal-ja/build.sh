#!/bin/bash
if [ "$1" == "" ]; then
  docker build . -t takaiyuk/ml-multimodal-ja-gpu -f ./Dockerfile
else
  docker build . -t $1 -f ./Dockerfile
fi
