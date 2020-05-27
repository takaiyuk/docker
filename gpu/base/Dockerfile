# docker build . -t takaiyuk/ml-base-gpu -f ./Dockerfile
# ref.) https://medium.com/the-artificial-impostor/smaller-docker-image-using-multi-stage-build-cb462e349968
FROM nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04 as builder
ARG PYTHON_VERSION=3.7.6
ARG CONDA_PYTHON_VERSION=3
ARG CONDA_DIR=/opt/conda
ENV PATH $CONDA_DIR/bin:$PATH
ENV PATH /usr/local/src/lightgbm/LightGBM:${PATH}
COPY requirements.txt .
# Instal basic utilities
RUN apt-get update \
  && apt-get install -y --no-install-recommends git wget unzip bzip2 build-essential ca-certificates cmake libboost-dev libboost-system-dev libboost-filesystem-dev gcc g++ \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  # Install miniconda
  && wget --quiet https://repo.continuum.io/miniconda/Miniconda$CONDA_PYTHON_VERSION-latest-Linux-x86_64.sh -O /tmp/miniconda.sh \
  && echo 'export PATH=$CONDA_DIR/bin:$PATH' > /etc/profile.d/conda.sh \
  && /bin/bash /tmp/miniconda.sh -b -p $CONDA_DIR \
  && rm -rf /tmp/* \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  # Install python packages
  && conda update -n base -c defaults conda \
  && conda config --add channels anaconda \
  && conda config --add channels conda-forge \
  && conda config --add channels pytorch \
  && conda install -y python=$PYTHON_VERSION \
  && conda install -y --file requirements.txt \
  && conda clean -tipsy \
  # LightGBM
  # ref.) https://github.com/microsoft/LightGBM/blob/master/docker/gpu/dockerfile.gpu
  && cd /usr/local/src && mkdir lightgbm && cd lightgbm \
  && git clone --recursive --branch stable --depth 1 https://github.com/microsoft/LightGBM \
  && cd LightGBM && mkdir build && cd build \
  && cmake -DUSE_GPU=1 -DOpenCL_LIBRARY=/usr/local/cuda/lib64/libOpenCL.so -DOpenCL_INCLUDE_DIR=/usr/local/cuda/include/ .. \
  && make OPENCL_HEADERS=/usr/local/cuda-10.2/targets/x86_64-linux/include LIBOPENCL=/usr/local/cuda-10.2/targets/x86_64-linux/lib \
  && /bin/bash -c "source activate $CONDA_VENV && cd /usr/local/src/lightgbm/LightGBM/python-package && python setup.py install --precompile && source deactivate"

FROM nvidia/cuda:10.2-base-ubuntu18.04 as runner
ARG CONDA_DIR=/opt/conda
ARG USERNAME=takaiyuk
ARG USERID=1000
ENV PATH $CONDA_DIR/bin:$PATH
ENV CUDA_HOME=/usr/local/cuda
ENV CUDA_ROOT=$CUDA_HOME
ENV PATH=$PATH:$CUDA_ROOT/bin:$HOME/bin
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CUDA_ROOT/lib64
# Instal basic utilities
RUN apt-get update \
  && apt-get install -y --no-install-recommends git wget unzip bzip2 sudo p7zip vim \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && mkdir -p /opt/conda/ \
  # Create the user
  && useradd --create-home -s /bin/bash --no-user-group -u $USERID $USERNAME \
  && chown $USERNAME $CONDA_DIR -R \
  && adduser $USERNAME sudo \
  && echo "$USERNAME ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER $USERNAME
WORKDIR /home/$USERNAME
# Docker cannot handle --chown=$USERID
COPY --chown=1000 --from=builder /opt/conda/. $CONDA_DIR
COPY --from=builder /usr/local/cuda/lib64/libOpenCL.so.1 /usr/local/cuda/lib64/libOpenCL.so.1
COPY --from=builder /usr/lib/x86_64-linux-gnu/libboost_system.so.1.65.1 /usr/local/cuda/lib64/libboost_system.so.1.65.1
COPY --from=builder /usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.65.1 /usr/local/cuda/lib64/libboost_filesystem.so.1.65.1
