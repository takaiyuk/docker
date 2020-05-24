# docker build . -t multimodal-gpu -f ./Dockerfile
# docker run -d --name ${CONTAIINER_NAME} -p 8888:8888 -v ${PWD}:/workspace/ multimodal-gpu
# docker exec -it ${CONTAINER_ID} /bin/bash
# jupyter notebook list
FROM pytorch/pytorch:latest
ARG PYTHON_VERSION=3.8
ENV APP_HOME /workspace
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR $APP_HOME
COPY requirements.txt $APP_HOME
COPY setup.py $APP_HOME
RUN apt-get update -y \
    && apt-get install -y clang cmake curl git libopencv-dev nodejs npm unzip vim wget \
    # fastText
    && pip install git+https://github.com/facebookresearch/fastText.git \
    # LighGBM
    && git clone --recursive https://github.com/microsoft/LightGBM && cd LightGBM && mkdir build && cd build && cmake .. && make -j4 && cd ../python-package && python setup.py install && cd ../.. && rm -r LightGBM \
    # requirements.txt
    && cd $APP_HOME \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    # jupyter extensions
    && export NODE_OPTIONS=--max-old-space-size=4096 \
    && conda install -yc conda-forge nodejs \
    && jupyter labextension install @jupyterlab/toc \
    && jupyter nbextension enable --py widgetsnbextension \
    # Clean
    && apt-get -y remove clang cmake curl nodejs npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
CMD jupyter lab \
    --no-browser \
    --port=8888 \
    --ip=0.0.0.0 \
    --allow-root

