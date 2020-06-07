# ./build.sh
# ./run.sh ${CONTAINER_NAME}
# ./exec.sh ${CONTAINER_NAME}
# . /venv/bin/activate && jupyter notebook list
FROM takaiyuk/ml-base-gpu:latest
ENV APP_HOME /workspace
ENV TZ Asia/Tokyo
ENV DEBIAN_FRONTEND noninteractive
WORKDIR $APP_HOME
COPY requirements.txt .
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime \
  && . /venv/bin/activate \
  && apt-get update -y \
  && apt-get install -y --no-install-recommends clang cmake gcc g++ libopencv-dev python3-dev \
  # fastText
  && pip install git+https://github.com/facebookresearch/fastText.git \
  # requirements.txt
  && cd $APP_HOME \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  # Clean
  && apt-get -y remove clang cmake gcc g++ python3-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
CMD . /venv/bin/activate \
  && jupyter lab \
  --port=8888 \
  --ip=0.0.0.0 \
  --allow-root
