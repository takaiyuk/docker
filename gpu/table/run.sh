#!/bin/bash
sudo docker run --runtime=nvidia -it -d --name $1 -p 8888:8888 -v ${PWD}:/workspace -v ${HOME}/.kaggle:/root/.kaggle/ takaiyuk/ml-table-gpu
