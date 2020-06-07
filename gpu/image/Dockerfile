# ./build.sh
# ./run.sh ${CONTAINER_NAME}
# ./exec.sh ${CONTAINER_NAME}
# . /venv/bin/activate && jupyter notebook list
FROM takaiyuk/ml-base-gpu:latest
ENV APP_HOME /workspace
ENV TZ Asia/Tokyo
WORKDIR $APP_HOME
COPY requirements.txt $APP_HOME
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime \
  && apt-get update -y \
  && apt-get install -y --no-install-recommends libopencv-dev \
  # requirements.txt
  && cd $APP_HOME \
  && . /venv/bin/activate \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  # Clean
  # && apt-get -y remove HOGE \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
CMD . /venv/bin/activate \
  && jupyter lab \
  --no-browser \
  --port=8888 \
  --ip=0.0.0.0 \
  --allow-root

# TEST
# import cv2
# import PIL
