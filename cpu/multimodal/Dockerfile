# docker build . -t takaiyuk/ml-multimodal -f ./Dockerfile
# docker run -d --name ${CONTAINER_NAME} -p 8888:8888 -v ${PWD}:/workspace/ takaiyuk/ml-multimodal
# docker exec -it ${CONTAINER_ID} /bin/bash
# jupyter notebook list
FROM takaiyuk/ml-base:latest
ENV APP_HOME /workspace
WORKDIR $APP_HOME
COPY requirements.txt $APP_HOME
RUN apt-get update -y \
  && apt-get install -y clang cmake g++ libopencv-dev \
  # fastText
  && pip install git+https://github.com/facebookresearch/fastText.git \
  # requirements.txt
  && cd $APP_HOME \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  # Clean
  && apt-get -y remove clang cmake g++ \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
CMD jupyter lab \
  --no-browser \
  --port=8888 \
  --ip=0.0.0.0 \
  --allow-root
