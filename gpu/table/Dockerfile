# ./build.sh
# ./run.sh ${CONTAINER_NAME}
# ./exec.sh ${CONTAINER_NAME}
# . /venv/bin/activate && jupyter notebook list
FROM takaiyuk/ml-base-gpu:latest
ENV APP_HOME /workspace
ENV TZ Asia/Tokyo
WORKDIR $APP_HOME
COPY requirements.txt $APP_HOME
RUN sudo ln -sf /usr/share/zoneinfo/$TZ /etc/localtime
#   && sudo apt-get -y update \
#   && sudo apt-get -y install hoge \
#   && pip install -r requirements.txt \
#   && sudo apt-get clean \
#   && sudo rm -rf /var/lib/apt/lists/*
CMD . /venv/bin/activate \
  && jupyter lab \
  --no-browser \
  --port=8888 \
  --ip=0.0.0.0 \
  --allow-root

# TEST
# import lightgbm as lgb; X = [[0,1,2],[3,4,5]]; y = [0,1]; m = lgb.LGBMClassifier(device="gpu", gpu_platform_id=0, gpu_device_id=0); m.fit(X,y)
# import tensorflow as tf; print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
