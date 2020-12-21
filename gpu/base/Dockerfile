FROM nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04 as builder
ENV PYTHON_VERSION=3.7.9
ENV PYENV_ROOT /root/.pyenv
ENV CUDA_VERSION=10.2
ENV CUDA_HOME /usr/local/cuda
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:${CUDA_HOME}/lib64
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/usr/local/cuda-$CUDA_VERSION/lib64
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/usr/local/lib
ENV LIGHTGBM_VERSION v3.0.0
ENV OPENCL_LIBRARIES /usr/local/cuda/lib64
ENV OPENCL_INCLUDE_DIR /usr/local/cuda/include
ENV PATH /usr/local/src/lightgbm/LightGBM:${PATH}
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
# basic utilities
RUN apt-get update -y \
  && apt-get install -y --no-install-recommends build-essential bzip2 ca-certificates cmake curl g++ gcc git libboost-filesystem-dev libboost-dev libboost-system-dev libffi-dev libssl-dev python3-dev python3-pip python3-setuptools tar virtualenv wget unzip zlib1g-dev \
  && apt-get install -y --no-install-recommends language-pack-ja-base language-pack-ja \
  && apt-get autoremove -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
# pyenv
RUN git clone https://github.com/pyenv/pyenv.git $PYENV_ROOT
ENV PATH $PYENV_ROOT/bin:$PATH
ENV PATH $PYENV_ROOT/shims:$PATH
RUN pyenv install -v $PYTHON_VERSION \
  && pyenv global $PYTHON_VERSION
# install
COPY requirements.txt .
RUN locale-gen en_US.UTF-8 \
  && python -m pip install -U pip \
  && pip install -U pip wheel \
  && pip install -r requirements.txt
# lightgbm
RUN mkdir -p /etc/OpenCL/vendors && echo "libnvidia-opencl.so.1" > /etc/OpenCL/vendors/nvidia.icd \
  && cd /usr/local/src && mkdir lightgbm && cd lightgbm \
  && git clone --recursive --branch stable --depth 1 https://github.com/microsoft/LightGBM -b $LIGHTGBM_VERSION \
  && cd LightGBM && mkdir build && cd build \
  && cmake -DUSE_GPU=1 -DOpenCL_LIBRARY=$OPENCL_LIBRARIES/libOpenCL.so -DOpenCL_INCLUDE_DIR=$OPENCL_INCLUDE_DIR/ .. \
  && make OPENCL_HEADERS=/usr/local/cuda-$CUDA_VERSION/targets/x86_64-linux/include LIBOPENCL=/usr/local/cuda-$CUDA_VERSION/targets/x86_64-linux/lib \
  && /bin/bash -c "cd /usr/local/src/lightgbm/LightGBM/python-package && python setup.py bdist_wheel -d /tmp/wheelhouse"
# build from source
RUN git clone https://github.com/cocodataset/cocoapi && cd cocoapi/PythonAPI && python setup.py build_ext bdist_wheel -d /tmp/wheelhouse && cd ../.. && rm -r cocoapi \
  && git clone https://github.com/pfnet-research/xfeat.git && cd xfeat && python setup.py bdist_wheel -d /tmp/wheelhouse && cd .. && rm -r xfeat

FROM rapidsai/rapidsai:cuda10.2-base-ubuntu18.04-py3.7 as rapidsai

FROM nvidia/cuda:10.2-cudnn7-runtime-ubuntu18.04 as runner
ENV PYTHON_VERSION=3.7.9
ENV PYENV_ROOT /root/.pyenv
ENV CUDA_VERSION=10.2
ENV CUDA_HOME /usr/local/cuda
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:${CUDA_HOME}/lib64
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:${CUDA_HOME}-${CUDA_VERSION}/lib64
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/usr/local/lib
ENV OPENCL_LIBRARIES ${CUDA_HOME}/lib64
ENV OPENCL_INCLUDE_DIR ${CUDA_HOME}/include
ENV PATH /usr/local/src/lightgbm/LightGBM:${PATH}
RUN apt-get update -y \
  && apt-get install -y --no-install-recommends build-essential bzip2 git libbz2-dev libffi-dev libssl-dev python3-dev python3-pip unzip vim virtualenv wget zip zlib1g-dev \
  && apt-get autoremove -y \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*
# pyenv
RUN git clone https://github.com/pyenv/pyenv.git $PYENV_ROOT
ENV PATH $PYENV_ROOT/bin:$PATH
ENV PATH $PYENV_ROOT/shims:$PATH
RUN pyenv install -v $PYTHON_VERSION \
  && pyenv global $PYTHON_VERSION
# install
COPY --from=builder $PYENV_ROOT/versions/$PYTHON_VERSION/lib/python3.7/site-packages $PYENV_ROOT/versions/$PYTHON_VERSION/lib/python3.7/site-packages
# lightgbm, cocoapi, xfeat
COPY --from=builder /tmp/wheelhouse /tmp/wheelhouse
RUN python -m pip install -U pip \
  && pip install -U pip wheel \
  && pip install --no-index /tmp/wheelhouse/*.whl \
  && rm -r /tmp \
  && mkdir /root/.kaggle
# lightgbm-lib
COPY --from=builder /etc/OpenCL/vendors/nvidia.icd /etc/OpenCL/vendors/nvidia.icd
COPY --from=builder /usr/lib/x86_64-linux-gnu/libgomp.so.1 $OPENCL_LIBRARIES/libgomp.so.1
COPY --from=builder /usr/lib/x86_64-linux-gnu/libboost_system.so.1.65.1 $OPENCL_LIBRARIES/libboost_system.so.1.65.1
COPY --from=builder /usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.65.1 $OPENCL_LIBRARIES/libboost_filesystem.so.1.65.1
COPY --from=builder $CUDA_HOME-$CUDA_VERSION/lib64/libOpenCL.so.1 $CUDA_HOME-$CUDA_VERSION/lib64/libOpenCL.so.1
# cupy-package
COPY --from=rapidsai /conda/envs/rapids/lib/python3.7/site-packages/cudf $PYENV_ROOT/versions/$PYTHON_VERSION/lib/python3.7/site-packages/cudf
COPY --from=rapidsai /conda/envs/rapids/lib/python3.7/site-packages/cupy $PYENV_ROOT/versions/$PYTHON_VERSION/lib/python3.7/site-packages/cupy
COPY --from=rapidsai /conda/envs/rapids/lib/python3.7/site-packages/cupy_backends $PYENV_ROOT/versions/$PYTHON_VERSION/lib/python3.7/site-packages/cupy_backends
COPY --from=rapidsai /conda/envs/rapids/lib/python3.7/site-packages/cupyx $PYENV_ROOT/versions/$PYTHON_VERSION/lib/python3.7/site-packages/cupyx
COPY --from=rapidsai /conda/envs/rapids/lib/python3.7/site-packages/fastrlock $PYENV_ROOT/versions/$PYTHON_VERSION/lib/python3.7/site-packages/fastrlock
COPY --from=rapidsai /conda/envs/rapids/lib/python3.7/site-packages/nvtx $PYENV_ROOT/versions/$PYTHON_VERSION/lib/python3.7/site-packages/nvtx
COPY --from=rapidsai /conda/envs/rapids/lib/python3.7/site-packages/pyarrow $PYENV_ROOT/versions/$PYTHON_VERSION/lib/python3.7/site-packages/pyarrow
COPY --from=rapidsai /conda/envs/rapids/lib/python3.7/site-packages/rmm $PYENV_ROOT/versions/$PYTHON_VERSION/lib/python3.7/site-packages/rmm
COPY --from=rapidsai /conda/envs/rapids/lib/python3.7/site-packages/cuml $PYENV_ROOT/versions/$PYTHON_VERSION/lib/python3.7/site-packages/cuml
COPY --from=rapidsai /conda/envs/rapids/lib/python3.7/site-packages/treelite $PYENV_ROOT/versions/$PYTHON_VERSION/lib/python3.7/site-packages/treelite
# cupy-lib
COPY --from=rapidsai /conda/envs/rapids/lib/libarrow.so.100 $CUDA_HOME-$CUDA_VERSION/lib64/libarrow.so.100
COPY --from=rapidsai /conda/envs/rapids/lib/libarrow_cuda.so.100 $CUDA_HOME-$CUDA_VERSION/lib64/libarrow_cuda.so.100
COPY --from=rapidsai /conda/envs/rapids/lib/libarrow_flight.so.100 $CUDA_HOME-$CUDA_VERSION/lib64/libarrow_flight.so.100
COPY --from=rapidsai /conda/envs/rapids/lib/libarrow_python.so.100 $CUDA_HOME-$CUDA_VERSION/lib64/libarrow_python.so.100
COPY --from=rapidsai /conda/envs/rapids/lib/libboost_filesystem.so.1.72.0 $CUDA_HOME-$CUDA_VERSION/lib64/libboost_filesystem.so.1.72.0
COPY --from=rapidsai /conda/envs/rapids/lib/libcares.so.2 $CUDA_HOME-$CUDA_VERSION/lib64/libcares.so.2
COPY --from=rapidsai /conda/envs/rapids/lib/libcudf.so $CUDA_HOME-$CUDA_VERSION/lib64/libcudf.so
COPY --from=rapidsai /conda/envs/rapids/lib/libgflags.so.2.2 $CUDA_HOME-$CUDA_VERSION/lib64/libgflags.so.2.2
COPY --from=rapidsai /conda/envs/rapids/lib/libglog.so.0 $CUDA_HOME-$CUDA_VERSION/lib64/libglog.so.0
COPY --from=rapidsai /conda/envs/rapids/lib/libprotobuf.so.24 $CUDA_HOME-$CUDA_VERSION/lib64/libprotobuf.so.24
COPY --from=rapidsai /conda/envs/rapids/lib/libsnappy.so.1 $CUDA_HOME-$CUDA_VERSION/lib64/libsnappy.so.1
COPY --from=rapidsai /conda/envs/rapids/lib/liburiparser.so $CUDA_HOME-$CUDA_VERSION/lib64/liburiparser.so
COPY --from=rapidsai /conda/envs/rapids/lib/libcudart.so.10.2 $CUDA_HOME/lib64/libcudart.so.10.1
COPY --from=rapidsai /conda/envs/rapids/lib/libcudf_ast.so $CUDA_HOME-$CUDA_VERSION/lib64/libcudf_ast.so
COPY --from=rapidsai /conda/envs/rapids/lib/libcudf_comms.so $CUDA_HOME-$CUDA_VERSION/lib64/libcudf_comms.so
COPY --from=rapidsai /conda/envs/rapids/lib/libcudf_hash.so $CUDA_HOME-$CUDA_VERSION/lib64/libcudf_hash.so
COPY --from=rapidsai /conda/envs/rapids/lib/libcudf_interop.so $CUDA_HOME-$CUDA_VERSION/lib64/libcudf_interop.so
COPY --from=rapidsai /conda/envs/rapids/lib/libcudf_io.so $CUDA_HOME-$CUDA_VERSION/lib64/libcudf_io.so
COPY --from=rapidsai /conda/envs/rapids/lib/libcudf_join.so $CUDA_HOME-$CUDA_VERSION/lib64/libcudf_join.so
COPY --from=rapidsai /conda/envs/rapids/lib/libcudf_merge.so $CUDA_HOME-$CUDA_VERSION/lib64/libcudf_merge.so
COPY --from=rapidsai /conda/envs/rapids/lib/libcudf_partitioning.so $CUDA_HOME-$CUDA_VERSION/lib64/libcudf_partitioning.so
COPY --from=rapidsai /conda/envs/rapids/lib/libcudf_reductions.so $CUDA_HOME-$CUDA_VERSION/lib64/libcudf_reductions.so
COPY --from=rapidsai /conda/envs/rapids/lib/libcudf_replace.so $CUDA_HOME-$CUDA_VERSION/lib64/libcudf_replace.so
COPY --from=rapidsai /conda/envs/rapids/lib/libcudf_reshape.so $CUDA_HOME-$CUDA_VERSION/lib64/libcudf_reshape.so
COPY --from=rapidsai /conda/envs/rapids/lib/libcudf_rolling.so $CUDA_HOME-$CUDA_VERSION/lib64/libcudf_rolling.so
COPY --from=rapidsai /conda/envs/rapids/lib/libcudf_transpose.so $CUDA_HOME-$CUDA_VERSION/lib64/libcudf_transpose.so
COPY --from=rapidsai /conda/envs/rapids/lib/libcudf_base.so $CUDA_HOME-$CUDA_VERSION/lib64/libcudf_base.so
COPY --from=rapidsai /conda/envs/rapids/lib/libbrotlienc.so.1 $CUDA_HOME-$CUDA_VERSION/lib64/libbrotlienc.so.1
COPY --from=rapidsai /conda/envs/rapids/lib/libbrotlidec.so.1 $CUDA_HOME-$CUDA_VERSION/lib64/libbrotlidec.so.1
COPY --from=rapidsai /conda/envs/rapids/lib/liborc.so $CUDA_HOME-$CUDA_VERSION/lib64/liborc.so
COPY --from=rapidsai /conda/envs/rapids/lib/libaws-cpp-sdk-s3.so $CUDA_HOME-$CUDA_VERSION/lib64/libaws-cpp-sdk-s3.so
COPY --from=rapidsai /conda/envs/rapids/lib/libaws-cpp-sdk-core.so $CUDA_HOME-$CUDA_VERSION/lib64/libaws-cpp-sdk-core.so
COPY --from=rapidsai /conda/envs/rapids/lib/libutf8proc.so.2 $CUDA_HOME-$CUDA_VERSION/lib64/libutf8proc.so.2
COPY --from=rapidsai /conda/envs/rapids/lib/libbrotlicommon.so.1 $CUDA_HOME-$CUDA_VERSION/lib64/libbrotlicommon.so.1
COPY --from=rapidsai /conda/envs/rapids/lib/libcurl.so.4 $CUDA_HOME-$CUDA_VERSION/lib64/libcurl.so.4
COPY --from=rapidsai /conda/envs/rapids/lib/libaws-c-event-stream.so.0unstable $CUDA_HOME-$CUDA_VERSION/lib64/libaws-c-event-stream.so.0unstable
COPY --from=rapidsai /conda/envs/rapids/lib/libaws-c-common.so.1 $CUDA_HOME-$CUDA_VERSION/lib64/libaws-c-common.so.1
COPY --from=rapidsai /conda/envs/rapids/lib/libssh2.so.1 $CUDA_HOME-$CUDA_VERSION/lib64/libssh2.so.1
COPY --from=rapidsai /conda/envs/rapids/lib/libcom_err.so.3 $CUDA_HOME-$CUDA_VERSION/lib64/libcom_err.so.3
COPY --from=rapidsai /conda/envs/rapids/lib/libaws-checksums.so.1.0.0 $CUDA_HOME-$CUDA_VERSION/lib64/libaws-checksums.so.1.0.0
COPY --from=rapidsai /conda/envs/rapids/lib/liblz4.so $CUDA_HOME-$CUDA_VERSION/lib64/liblz4.so
COPY --from=rapidsai /conda/envs/rapids/lib/libarrow_dataset.so.100 $CUDA_HOME-$CUDA_VERSION/lib64/libarrow_dataset.so.100
COPY --from=rapidsai /conda/envs/rapids/lib/libparquet.so.100 $CUDA_HOME-$CUDA_VERSION/lib64/libparquet.so.100
COPY --from=rapidsai /conda/envs/rapids/lib/libthrift.so.0.13.0 $CUDA_HOME-$CUDA_VERSION/lib64/libthrift.so.0.13.0
COPY --from=rapidsai /conda/envs/rapids/lib/libcuml++.so $CUDA_HOME-$CUDA_VERSION/lib64/libcuml++.so
COPY --from=rapidsai /conda/envs/rapids/lib/libcumlprims.so $CUDA_HOME-$CUDA_VERSION/lib64/libcumlprims.so
COPY --from=rapidsai /conda/envs/rapids/lib/libfaiss.so $CUDA_HOME-$CUDA_VERSION/lib64/libfaiss.so
COPY --from=rapidsai /conda/envs/rapids/lib/libfaiss.so /opt/conda/envs/rapids/lib/
COPY --from=rapidsai /conda/envs/rapids/lib/libtreelite.so $CUDA_HOME-$CUDA_VERSION/lib64/libtreelite.so
COPY --from=rapidsai /conda/envs/rapids/lib/libblas.so.3 $CUDA_HOME-$CUDA_VERSION/lib64/libblas.so.3
COPY --from=rapidsai /conda/envs/rapids/lib/liblapack.so.3 $CUDA_HOME-$CUDA_VERSION/lib64/liblapack.so.3
COPY --from=rapidsai /conda/envs/rapids/lib/libgfortran.so.4 $CUDA_HOME-$CUDA_VERSION/lib64/libgfortran.so.4
