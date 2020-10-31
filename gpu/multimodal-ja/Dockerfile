FROM takaiyuk/ml-base-gpu:latest
ENV APP_HOME /workspace
ENV TZ Asia/Tokyo
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8
WORKDIR $APP_HOME
COPY requirements.txt .
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime \
  && . /venv/bin/activate \
  && apt-get update -y \
  && apt-get install -y --no-install-recommends build-essential cmake curl file python3-dev sudo language-pack-ja-base language-pack-ja\
  # MeCab
  && apt-get install -y --no-install-recommends mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8 \
  # mecab-ipadic-NEologd
  && git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git /tmp/neologd \
  && /tmp/neologd/bin/install-mecab-ipadic-neologd -n -a -y \
  && sed -i -e "s|^dicdir.*$|dicdir = /usr/lib/mecab/dic/mecab-ipadic-neologd|" /etc/mecabrc \
  && rm -rf /tmp/neologd \
  # fastText
  && git clone https://github.com/facebookresearch/fastText.git \
  && cd fastText \
  && python setup.py install \
  && cd .. \
  && rm -rf fastText
# requirements.txt
RUN . /venv/bin/activate \
  # for avoid UnicodeDecodeError when installing sudachiDict
  && locale-gen en_US.UTF-8 \
  && cd $APP_HOME \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  # Clean
  && apt-get -y remove build-essential cmake curl file python3-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
CMD . /venv/bin/activate \
  && jupyter lab \
  --no-browser \
  --port=8888 \
  --ip=0.0.0.0 \
  --allow-root
