# ./build.sh
# ./run.sh ${CONTAINER_NAME}
# ./exec.sh ${CONTAINER_NAME}
# . /venv/bin/activate && jupyter notebook list
FROM takaiyuk/ml-base-gpu:latest
ENV APP_HOME /workspace
ENV TZ Asia/Tokyo
# ENV DEBIAN_FRONTEND noninteractive
WORKDIR $APP_HOME
COPY requirements.txt .
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime \
  && . /venv/bin/activate \
  && apt-get update -y \
  && apt-get install -y --no-install-recommends clang cmake curl file gcc g++ libopencv-dev sudo unzip wget xz-utils zip python3-dev \
  # MeCab
  && apt-get install -y --no-install-recommends mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8 \
  # mecab-ipadic-NEologd
  && git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git /tmp/neologd \
  && /tmp/neologd/bin/install-mecab-ipadic-neologd -n -a -y \
  && sed -i -e "s|^dicdir.*$|dicdir = /usr/lib/mecab/dic/mecab-ipadic-neologd|" /etc/mecabrc \
  && rm -rf /tmp/neologd \
  # # CRF++
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
  # requirements.txt
  && cd $APP_HOME \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  # Clean
  && apt-get -y remove clang cmake curl file gcc g++ xz-utils zip python3-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
CMD . /venv/bin/activate \
  && jupyter lab \
  --no-browser \
  --port=8888 \
  --ip=0.0.0.0 \
  --allow-root
