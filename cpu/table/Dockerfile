# ./build.sh
# ./run.sh ${CONTAINER_NAME}
# ./exec.sh ${CONTAINER_NAME}
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
