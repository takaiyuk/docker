# ./build.sh
FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04 as builder
ARG PYTHON_VERSION=3.6.9
ARG CUDA_VERSION=10.1
ENV CUDA_HOME /usr/local/cuda
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:${CUDA_HOME}/lib64
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/usr/local/cuda-$CUDA_VERSION/lib64
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/usr/local/lib
ENV OPENCL_LIBRARIES /usr/local/cuda/lib64
ENV OPENCL_INCLUDE_DIR /usr/local/cuda/include
ENV PATH /usr/local/src/lightgbm/LightGBM:${PATH}
ENV TORCH_VERSION=1.6.0
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
COPY requirements.txt .
# Instal basic utilities
RUN apt-get update -y \
  && apt-get install -y --no-install-recommends build-essential bzip2 ca-certificates cmake g++ gcc git libboost-filesystem-dev libboost-dev libboost-system-dev libffi-dev libssl-dev python3-dev python3-pip python3-setuptools virtualenv wget unzip \
  && apt-get install -y --no-install-recommends language-pack-ja-base language-pack-ja \
  && apt-get autoremove -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && virtualenv -p python3 ./venv
RUN . /venv/bin/activate \
  && locale-gen en_US.UTF-8 \
  && pip install -U pip wheel \
  && pip wheel -w /tmp/wheelhouse -r requirements.txt \
  && pip install --no-index /tmp/wheelhouse/*.whl
RUN . /venv/bin/activate \
  # Install pytorch
  && pip wheel -w /tmp/wheelhouse torch-scatter==latest+cu101 torch-sparse==latest+cu101 -f https://pytorch-geometric.com/whl/torch-$TORCH_VERSION.html \
  && pip wheel -w /tmp/wheelhouse torch-geometric
RUN . /venv/bin/activate \
  # Install LightGBM (ref. https://github.com/microsoft/LightGBM/blob/master/docker/gpu/dockerfile.gpu)
  # Add OpenCL ICD files for LightGBM
  && mkdir -p /etc/OpenCL/vendors && echo "libnvidia-opencl.so.1" > /etc/OpenCL/vendors/nvidia.icd \
  && cd /usr/local/src && mkdir lightgbm && cd lightgbm \
  && git clone --recursive --branch stable --depth 1 https://github.com/microsoft/LightGBM \
  && cd LightGBM && mkdir build && cd build \
  && cmake -DUSE_GPU=1 -DOpenCL_LIBRARY=$OPENCL_LIBRARIES/libOpenCL.so -DOpenCL_INCLUDE_DIR=$OPENCL_INCLUDE_DIR/ .. \
  && make OPENCL_HEADERS=/usr/local/cuda-$CUDA_VERSION/targets/x86_64-linux/include LIBOPENCL=/usr/local/cuda-$CUDA_VERSION/targets/x86_64-linux/lib \
  && /bin/bash -c "cd /usr/local/src/lightgbm/LightGBM/python-package && python setup.py bdist_wheel -d /tmp/wheelhouse"
RUN . /venv/bin/activate \
  # Install cocoapi
  && pip wheel -w /tmp/wheelhouse Cython \
  && pip install --no-index /tmp/wheelhouse/Cython-*.whl \
  && git clone https://github.com/cocodataset/cocoapi && cd cocoapi/PythonAPI && python setup.py build_ext bdist_wheel -d /tmp/wheelhouse && cd ../.. && rm -r cocoapi \
  # Install xfeat
  && git clone https://github.com/pfnet-research/xfeat.git && cd xfeat && python setup.py bdist_wheel -d /tmp/wheelhouse && cd .. && rm -r xfeat
RUN . /venv/bin/activate \
  # Solve double requirement(e.g. require h5py<3.0.0 but keras install latest h5py, so remove it)
  && rm /tmp/wheelhouse/h5py-3*.whl /tmp/wheelhouse/urllib3-1.26.0*.whl

FROM rapidsai/rapidsai:0.14-cuda10.1-base-ubuntu18.04-py3.6 as rapidsai

FROM nvidia/cuda:10.1-cudnn7-runtime-ubuntu18.04 as runner
ARG PYTHON_VERSION=3.6.9
ARG CUDA_VERSION=10.1
ENV CUDA_HOME /usr/local/cuda
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:${CUDA_HOME}/lib64
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:${CUDA_HOME}-${CUDA_VERSION}/lib64
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/usr/local/lib
ENV OPENCL_LIBRARIES ${CUDA_HOME}/lib64
ENV OPENCL_INCLUDE_DIR ${CUDA_HOME}/include
ENV PATH /usr/local/src/lightgbm/LightGBM:${PATH}
COPY --from=builder /tmp/wheelhouse /tmp/wheelhouse
RUN apt-get update -y \
  && apt-get install -y --no-install-recommends git unzip vim virtualenv wget zip \
  && apt-get autoremove -y \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/* \
  && virtualenv -p python3 ./venv
RUN . /venv/bin/activate \
  && pip install -U pip wheel \
  && pip install --no-index /tmp/wheelhouse/*.whl \
  && rm -r /tmp/wheelhouse \
  && mkdir /root/.kaggle
# copy for LightGBM
COPY --from=builder /etc/OpenCL/vendors/nvidia.icd /etc/OpenCL/vendors/nvidia.icd
COPY --from=builder /usr/lib/x86_64-linux-gnu/libgomp.so.1 $OPENCL_LIBRARIES/libgomp.so.1
COPY --from=builder /usr/lib/x86_64-linux-gnu/libboost_system.so.1.65.1 $OPENCL_LIBRARIES/libboost_system.so.1.65.1
COPY --from=builder /usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.65.1 $OPENCL_LIBRARIES/libboost_filesystem.so.1.65.1
COPY --from=builder /usr/local/cuda-10.1/lib64/libOpenCL.so.1 /usr/local/cuda-10.1/lib64/libOpenCL.so.1
# copy for cudf-package
COPY --from=rapidsai /conda/envs/rapids/lib/python3.6/site-packages/cudf /venv/lib/python3.6/site-packages/cudf
COPY --from=rapidsai /conda/envs/rapids/lib/python3.6/site-packages/cupy /venv/lib/python3.6/site-packages/cupy
COPY --from=rapidsai /conda/envs/rapids/lib/python3.6/site-packages/cupyx /venv/lib/python3.6/site-packages/cupyx
COPY --from=rapidsai /conda/envs/rapids/lib/python3.6/site-packages/fastrlock /venv/lib/python3.6/site-packages/fastrlock
COPY --from=rapidsai /conda/envs/rapids/lib/python3.6/site-packages/rmm /venv/lib/python3.6/site-packages/rmm
# copy for cudf-lib
COPY --from=rapidsai /conda/envs/rapids/lib/libarrow.so.15 /usr/local/cuda-10.1/lib64/libarrow.so.15
COPY --from=rapidsai /conda/envs/rapids/lib/libarrow_flight.so.15 /usr/local/cuda-10.1/lib64/libarrow_flight.so.15
COPY --from=rapidsai /conda/envs/rapids/lib/libarrow_python.so.15 /usr/local/cuda-10.1/lib64/libarrow_python.so.15
COPY --from=rapidsai /conda/envs/rapids/lib/libboost_filesystem.so.1.70.0 /usr/local/cuda-10.1/lib64/libboost_filesystem.so.1.70.0
COPY --from=rapidsai /conda/envs/rapids/lib/libcares.so.2 /usr/local/cuda-10.1/lib64/libcares.so.2
COPY --from=rapidsai /conda/envs/rapids/lib/libcudf.so /usr/local/cuda-10.1/lib64/libcudf.so
COPY --from=rapidsai /conda/envs/rapids/lib/libgflags.so.2.2 /usr/local/cuda-10.1/lib64/libgflags.so.2.2
COPY --from=rapidsai /conda/envs/rapids/lib/libglog.so.0 /usr/local/cuda-10.1/lib64/libglog.so.0
COPY --from=rapidsai /conda/envs/rapids/lib/libprotobuf.so.19 /usr/local/cuda-10.1/lib64/libprotobuf.so.19
COPY --from=rapidsai /conda/envs/rapids/lib/librmm.so /usr/local/cuda-10.1/lib64/librmm.so
COPY --from=rapidsai /conda/envs/rapids/lib/libsnappy.so.1 /usr/local/cuda-10.1/lib64/libsnappy.so.1
COPY --from=rapidsai /conda/envs/rapids/lib/liburiparser.so.1 /usr/local/cuda-10.1/lib64/liburiparser.so.1
