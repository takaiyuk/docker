# docker build . -t takaiyuk/ml-multimodal-gpu -f ./Dockerfile
# docker run -d --name ${CONTAINER_NAME} -p 8888:8888 -v ${PWD}:/workspace/ takaiyuk/ml-multimodal-gpu
# docker exec -it ${CONTAINER_ID} /bin/bash
# jupyter notebook list
FROM takaiyuk/ml-base-gpu:latest
ENV APP_HOME /workspace
ENV TZ Asia/Tokyo
ENV DEBIAN_FRONTEND noninteractive
WORKDIR $APP_HOME
COPY requirements.txt $APP_HOME
RUN sudo ln -sf /usr/share/zoneinfo/$TZ /etc/localtime \
  && sudo apt-get update -y \
  && sudo apt-get install -y --no-install-recommends clang cmake g++ libopencv-dev \
  # fastText
  && pip install git+https://github.com/facebookresearch/fastText.git \
  # requirements.txt
  && cd $APP_HOME \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  # Clean
  && sudo apt-get -y remove clang cmake g++ \
  && sudo apt-get clean \
  && sudo rm -rf /var/lib/apt/lists/*
CMD jupyter lab \
  --no-browser \
  --port=8888 \
  --ip=0.0.0.0 \
  --allow-root
