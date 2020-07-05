#!/bin/bash
sudo docker run --rm -it -p 5000:5000 -v ${PWD}:/workspace takaiyuk/ml-mlflow
