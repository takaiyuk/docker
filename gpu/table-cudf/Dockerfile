FROM rapidsai/rapidsai:0.14-cuda10.1-base-ubuntu18.04-py3.6 as builder

FROM takaiyuk/ml-base-gpu:latest
ENV APP_HOME /workspace
ENV TZ Asia/Tokyo
WORKDIR $APP_HOME
COPY --from=builder /conda/envs/rapids/lib/python3.6/site-packages/cudf /venv/lib/python3.6/site-packages/cudf
COPY --from=builder /conda/envs/rapids/lib/python3.6/site-packages/cupy /venv/lib/python3.6/site-packages/cupy
COPY --from=builder /conda/envs/rapids/lib/python3.6/site-packages/cupyx /venv/lib/python3.6/site-packages/cupyx
COPY --from=builder /conda/envs/rapids/lib/python3.6/site-packages/fastrlock /venv/lib/python3.6/site-packages/fastrlock
COPY --from=builder /conda/envs/rapids/lib/python3.6/site-packages/pyarrow /venv/lib/python3.6/site-packages/pyarrow
COPY --from=builder /conda/envs/rapids/lib/python3.6/site-packages/rmm /venv/lib/python3.6/site-packages/rmm
COPY --from=builder /conda/envs/rapids/lib/libboost_filesystem.so.1.70.0 /usr/local/cuda-10.1/lib64/libboost_filesystem.so.1.70.0
COPY --from=builder /conda/envs/rapids/lib/libcudf.so /usr/local/cuda-10.1/lib64/libcudf.so
COPY --from=builder /conda/envs/rapids/lib/librmm.so /usr/local/cuda-10.1/lib64/librmm.so
# COPY --from=builder /conda/envs/rapids/lib/libarrow.so.15 /usr/local/cuda-10.1/lib64/libarrow.so.15
# COPY --from=builder /conda/envs/rapids/lib/libarrow_python.so.15 /usr/local/cuda-10.1/lib64/libarrow_python.so.15
# COPY --from=builder /conda/envs/rapids/lib/libglog.so.0 /usr/local/cuda-10.1/lib64/libglog.so.0
# COPY --from=builder /conda/envs/rapids/lib/liburiparser.so.1 /usr/local/cuda-10.1/lib64/liburiparser.so.1
# COPY --from=builder /conda/envs/rapids/lib/libsnappy.so.1 /usr/local/cuda-10.1/lib64/libsnappy.so.1
# COPY --from=builder /conda/envs/rapids/lib/libprotobuf.so.19 /usr/local/cuda-10.1/lib64/libprotobuf.so.19
# COPY --from=builder /conda/envs/rapids/lib/libarrow_flight.so.15 /usr/local/cuda-10.1/lib64/libarrow_flight.so.15
# COPY --from=builder /conda/envs/rapids/lib/libgflags.so.2.2 /usr/local/cuda-10.1/lib64/libgflags.so.2.2
# COPY --from=builder /conda/envs/rapids/lib/libcares.so.2 /usr/local/cuda-10.1/lib64/libcares.so.2
COPY requirements.txt $APP_HOME
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime \
  && apt-get -y update \
  # && sudo apt-get -y install HOGE \
  && . /venv/bin/activate \
  && pip install -r requirements.txt \
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
# import lightgbm as lgb; X = [[0,1,2],[3,4,5]]; y = [0,1]; m = lgb.LGBMClassifier(device="gpu", gpu_platform_id=0, gpu_device_id=0); m.fit(X,y)
# import tensorflow as tf; print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

# . /venv/bin/activate && python -c "import cudf"
