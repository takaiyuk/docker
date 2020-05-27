# docker build . -t takaiyuk/ml-table -f ./Dockerfile
# docker run -d --name ${CONTAINER_NAME} -p 8888:8888 -v ${PWD}:/workspace/ -v ${HOME}/.kaggle:/root/.kaggle/ takaiyuk/ml-table
# docker exec -it ${CONTAINER_ID} /bin/bash
# jupyter notebook list
FROM takaiyuk/ml-base:latest
ENV APP_HOME /workspace
WORKDIR $APP_HOME
# COPY requirements.txt $APP_HOME
# RUN apt-get -y update \
#   && apt-get -y install hoge \
#   && pip install -r requirements.txt \
#   && apt-get clean \
#   && rm -rf /var/lib/apt/lists/*
CMD jupyter lab \
  --no-browser \
  --port=8888 \
  --ip=0.0.0.0 \
  --allow-root
