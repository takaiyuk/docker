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
ENV TF_VERSION=2.2.0
ENV TORCH_VERSION=1.6.0
COPY requirements.txt .
# Instal basic utilities
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential bzip2 ca-certificates cmake git libboost-filesystem-dev libboost-dev libboost-system-dev libffi-dev libssl-dev python3-dev python3-pip python3-setuptools virtualenv wget unzip \
  && apt-get autoremove -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && virtualenv -p python3 ./venv
RUN . ./venv/bin/activate \
  && pip install -U pip \
  # Install pytorch
  && pip install -U tensorflow==$TF_VERSION \
  && pip install torch==$TORCH_VERSION torchvision \
  && pip install torch-scatter==latest+cu102 torch-sparse==latest+cu102 -f https://pytorch-geometric.com/whl/torch-$TORCH_VERSION.html \
  && pip install torch-geometric \
  # Install cocoapi
  && pip install Cython \
  && mkdir coco && cd coco && git clone https://github.com/cocodataset/cocoapi && cd cocoapi/PythonAPI && make install && cd ../.. && rm -r cocoapi \
  # Install xfeat
  && git clone https://github.com/pfnet-research/xfeat.git && cd xfeat && python setup.py install && cd .. && rm -r xfeat \
  # Add OpenCL ICD files for LightGBM
  && mkdir -p /etc/OpenCL/vendors && echo "libnvidia-opencl.so.1" > /etc/OpenCL/vendors/nvidia.icd \
  # LightGBM (ref.) https://github.com/microsoft/LightGBM/blob/master/docker/gpu/dockerfile.gpu
  && cd /usr/local/src && mkdir lightgbm && cd lightgbm \
  && git clone --recursive --branch stable --depth 1 https://github.com/microsoft/LightGBM \
  && cd LightGBM && mkdir build && cd build \
  && cmake -DUSE_GPU=1 -DOpenCL_LIBRARY=/usr/local/cuda/lib64/libOpenCL.so -DOpenCL_INCLUDE_DIR=/usr/local/cuda/include/ .. \
  && make OPENCL_HEADERS=/usr/local/cuda-$CUDA_VERSION/targets/x86_64-linux/include LIBOPENCL=/usr/local/cuda-$CUDA_VERSION/targets/x86_64-linux/lib \
  && /bin/bash -c "cd /usr/local/src/lightgbm/LightGBM/python-package && python setup.py install --precompile"
RUN . ./venv/bin/activate \
  && pip install -r requirements.txt

FROM nvidia/cuda:10.1-cudnn7-runtime-ubuntu18.04 as runner
ARG PYTHON_VERSION=3.6.9
ARG CUDA_VERSION=10.1
ENV CUDA_HOME /usr/local/cuda
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:${CUDA_HOME}/lib64
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/usr/local/cuda-$CUDA_VERSION/lib64
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/usr/local/lib
ENV OPENCL_LIBRARIES /usr/local/cuda/lib64
ENV OPENCL_INCLUDE_DIR /usr/local/cuda/include
ENV PATH /usr/local/src/lightgbm/LightGBM:${PATH}
RUN apt-get update \
  && apt-get install -y --no-install-recommends virtualenv git unzip vim wget zip \
  && apt-get autoremove -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && virtualenv -p python3 ./venv \
  && . ./venv/bin/activate \
  && mkdir /root/.kaggle
COPY --from=builder /venv /venv
COPY --from=builder /etc/OpenCL/vendors/nvidia.icd /etc/OpenCL/vendors/nvidia.icd
COPY --from=builder /usr/lib/x86_64-linux-gnu/libgomp.so.1 /usr/local/cuda/lib64/libgomp.so.1
COPY --from=builder /usr/lib/x86_64-linux-gnu/libboost_system.so.1.65.1 /usr/local/cuda/lib64/libboost_system.so.1.65.1
COPY --from=builder /usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.65.1 /usr/local/cuda/lib64/libboost_filesystem.so.1.65.1
COPY --from=builder /usr/local/cuda-10.1/lib64/libOpenCL.so.1 /usr/local/cuda-10.1/lib64/libOpenCL.so.1
COPY --from=builder /usr/local/cuda-10.1/targets/x86_64-linux/include /usr/local/cuda-10.1/targets/x86_64-linux/include
COPY --from=builder /usr/local/cuda-10.1/targets/x86_64-linux/lib /usr/local/cuda-10.1/targets/x86_64-linux/lib
