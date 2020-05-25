# docker build . -t multimodal -f ./Dockerfile
# docker run -d --name ${CONTAIINER_NAME} -p 8888:8888 -v ${PWD}:/workspace/ multimodal
# docker exec -it ${CONTAINER_ID} /bin/bash
# jupyter notebook list
FROM python:3.7.7-slim
ENV APP_HOME /workspace
WORKDIR $APP_HOME
COPY requirements.txt $APP_HOME
COPY setup.py $APP_HOME
RUN apt-get update -y \
    && apt-get install -y clang cmake curl git libopencv-dev nodejs npm unzip vim wget \
    # fastText
    && pip install git+https://github.com/facebookresearch/fastText.git \
    # LighGBM
    && git clone --recursive https://github.com/microsoft/LightGBM && cd LightGBM && mkdir build && cd build && cmake .. && make -j4 && cd ../python-package && python setup.py install && cd ../.. && rm -r LightGBM \
    # XGBoost
    && git clone --recursive https://github.com/dmlc/xgboost && cd xgboost && mkdir build && cd build && cmake .. && make -j$(nproc) && cd ../python-package && python setup.py install && cd ../.. && rm -r xgboost \
    # requirements.txt
    && cd $APP_HOME \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    # jupyter extensions
    && export NODE_OPTIONS=--max-old-space-size=4096 \
    && jupyter labextension install @jupyterlab/toc \
    && jupyter nbextension enable --py widgetsnbextension \
    # Clean
    && apt-get -y remove clang cmake nodejs npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
CMD jupyter lab \
    --no-browser \
    --port=8888 \
    --ip=0.0.0.0 \
    --allow-root
