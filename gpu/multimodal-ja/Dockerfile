# docker build . -t takaiyuk/ml-multimodal-ja-gpu -f ./Dockerfile
# docker run -d --name ${CONTAINER_NAME} -p 8888:8888 -v ${PWD}:/workspace/ takaiyuk/ml-multimodal-ja-gpu
# docker exec -it ${CONTAINER_ID} /bin/bash
# jupyter notebook list
FROM takaiyuk/ml-base-gpu:latest
ENV APP_HOME /workspace
ENV TZ Asia/Tokyo
ENV DEBIAN_FRONTEND noninteractive
WORKDIR $APP_HOME
COPY requirements.txt $APP_HOME
RUN sudo ln -sf /usr/share/zoneinfo/$TZ /etc/localtime \
    && sudo apt-get update -y \
    && sudo apt-get install -y --no-install-recommends clang cmake curl file git libopencv-dev sudo unzip vim wget xz-utils zip \
    # MeCab
    && sudo apt-get install -y --no-install-recommends mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8 \
    # mecab-ipadic-NEologd
    && git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git /tmp/neologd \
    && sudo /tmp/neologd/bin/install-mecab-ipadic-neologd -n -a -y \
    && sudo sed -i -e "s|^dicdir.*$|dicdir = /usr/lib/mecab/dic/mecab-ipadic-neologd|" /etc/mecabrc \
    && sudo rm -rf /tmp/neologd \
    # CRF++
    && sudo wget -O /tmp/CRF++-0.58.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7QVR6VXJ5dWExSTQ" \
    && cd /tmp \
    && sudo tar zxf CRF++-0.58.tar.gz \
    && cd CRF++-0.58 \
    && sudo ./configure \
    && sudo make \
    && sudo make install \
    && cd / \
    && sudo rm /tmp/CRF++-0.58.tar.gz \
    && sudo rm -rf /tmp/CRF++-0.58 \
    && sudo ldconfig \
    # CaboCha
    && cd /tmp \
    && sudo curl -c cabocha-0.69.tar.bz2 -s -L "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7SDd1Q1dUQkZQaUU" \
    | sudo grep confirm | sed -e "s/^.*confirm=\(.*\)&amp;id=.*$/\1/" \
    | xargs -I{} curl -b  cabocha-0.69.tar.bz2 -L -o cabocha-0.69.tar.bz2 \
    "https://drive.google.com/uc?confirm={}&export=download&id=0B4y35FiV1wh7SDd1Q1dUQkZQaUU" \
    && sudo tar jxf cabocha-0.69.tar.bz2 \
    && cd cabocha-0.69 \
    && sudo export CPPFLAGS=-I/usr/local/include \
    && sudo ./configure --with-mecab-config=`which mecab-config` --with-charset=utf8 \
    && sudo make \
    && sudo make install \
    && cd python \
    && sudo python setup.py build \
    && sudo python setup.py install \
    && cd / \
    && sudo rm /tmp/cabocha-0.69.tar.bz2 \
    && sudo rm -rf /tmp/cabocha-0.69 \
    && sudo ldconfig \
    # fastText
    && pip install git+https://github.com/facebookresearch/fastText.git \
    # requirements.txt
    && cd $APP_HOME \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    # Clean
    && sudo apt-get -y remove clang cmake curl file xz-utils zip \
    && sudo apt-get clean \
    && sudo rm -rf /var/lib/apt/lists/*
CMD jupyter lab \
    --no-browser \
    --port=8888 \
    --ip=0.0.0.0 \
    --allow-root















# docker build . -t multimodal-ja-gpu -f ./Dockerfile
# docker run -d --name ${CONTAINER_NAME} -p 8888:8888 -v ${PWD}:/workspace/ multimodal-ja-gpu
# docker exec -it ${CONTAINER_ID} /bin/bash
# jupyter notebook list
FROM pytorch/pytorch:latest
ARG PYTHON_VERSION=3.8
ENV APP_HOME /workspace
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR $APP_HOME
COPY requirements.txt $APP_HOME
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends clang cmake curl file git libopencv-dev nodejs npm sudo unzip vim wget xz-utils zip \
    # MeCab
    && apt-get install -y --no-install-recommends mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8 \
    # mecab-ipadic-NEologd
    && git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git /tmp/neologd \
    && /tmp/neologd/bin/install-mecab-ipadic-neologd -n -a -y \
    && sed -i -e "s|^dicdir.*$|dicdir = /usr/lib/mecab/dic/mecab-ipadic-neologd|" /etc/mecabrc \
    && rm -rf /tmp/neologd \
    # CRF++
    && wget -O /tmp/CRF++-0.58.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7QVR6VXJ5dWExSTQ" \
    && cd /tmp \
    && tar zxf CRF++-0.58.tar.gz \
    && cd CRF++-0.58 \ 
    && ./configure \
    && make \
    && make install \
    && cd / \
    && rm /tmp/CRF++-0.58.tar.gz \
    && rm -rf /tmp/CRF++-0.58 \
    && ldconfig \
    # CaboCha
    && cd /tmp \
    && curl -c cabocha-0.69.tar.bz2 -s -L "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7SDd1Q1dUQkZQaUU" \
    | grep confirm | sed -e "s/^.*confirm=\(.*\)&amp;id=.*$/\1/" \
    | xargs -I{} curl -b  cabocha-0.69.tar.bz2 -L -o cabocha-0.69.tar.bz2 \
    "https://drive.google.com/uc?confirm={}&export=download&id=0B4y35FiV1wh7SDd1Q1dUQkZQaUU" \
    && tar jxf cabocha-0.69.tar.bz2 \
    && cd cabocha-0.69 \
    && export CPPFLAGS=-I/usr/local/include \
    && ./configure --with-mecab-config=`which mecab-config` --with-charset=utf8 \
    && make \
    && make install \
    && cd python \
    && python setup.py build \
    && python setup.py install \
    && cd / \
    && rm /tmp/cabocha-0.69.tar.bz2 \
    && rm -rf /tmp/cabocha-0.69 \
    && ldconfig \
    # fastText
    && pip install git+https://github.com/facebookresearch/fastText.git \
    # LightGBM GPU
    && cd /usr/local/src && mkdir lightgbm && cd lightgbm \
    && git clone --recursive --branch stable --depth 1 https://github.com/microsoft/LightGBM \
    && cd LightGBM && mkdir build && cd build \
    && cmake -DUSE_GPU=1 -DOpenCL_LIBRARY=/usr/local/cuda/lib64/libOpenCL.so -DOpenCL_INCLUDE_DIR=/usr/local/cuda/include/ .. \
    && make OPENCL_HEADERS=/usr/local/cuda-8.0/targets/x86_64-linux/include LIBOPENCL=/usr/local/cuda-8.0/targets/x86_64-linux/lib \
    && /bin/bash -c "cd /usr/local/src/lightgbm/LightGBM/python-package && python setup.py install --precompile" \
    && rm -r /usr/local/src/lightgbm \
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
    && apt-get -y remove clang cmake curl file nodejs npm xz-utils zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
CMD jupyter lab \
    --no-browser \
    --port=8888 \
    --ip=0.0.0.0 \
    --allow-root

