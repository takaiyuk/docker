FROM takaiyuk/ml-base-gpu:latest
ENV PYTHON_VERSION=3.8
ENV APP_HOME /workspace
ENV TZ Asia/Tokyo
WORKDIR $APP_HOME
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime \
  && . /venv/bin/activate \
  && apt-get update -y \
  && apt-get install -y --no-install-recommends build-essential cmake curl file g++ gcc python$PYTHON_VERSION-dev sudo language-pack-ja-base language-pack-ja
RUN . /venv/bin/activate \
  && pip install -U pip \
  # for Opencv
  && apt-get install -y --no-install-recommends libopencv-dev \
  # MeCab
  && apt-get install -y --no-install-recommends mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8 \
  # mecab-ipadic-NEologd
  && git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git /tmp/neologd \
  && /tmp/neologd/bin/install-mecab-ipadic-neologd -n -a -y \
  && sed -i -e "s|^dicdir.*$|dicdir = /usr/lib/mecab/dic/mecab-ipadic-neologd|" /etc/mecabrc \
  && rm -rf /tmp/neologd \
  # fastText
  && git clone https://github.com/facebookresearch/fastText.git && cd fastText && pip install . && cd .. && rm -rf fastText
ENV POETRY_VERSION 1.1.6
RUN . /venv/bin/activate \
  && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/$POETRY_VERSION/get-poetry.py | python
ENV PATH /root/.poetry/bin:$PATH
COPY poetry.lock pyproject.toml ./
COPY multimodal_ja/ ./multimodal_ja/
RUN . /venv/bin/activate \
  # for avoid UnicodeDecodeError when installing sudachiDict
  && locale-gen en_US.UTF-8 \
  && poetry install --no-interaction --no-ansi --no-dev
RUN . /venv/bin/activate \
  && poetry build \
  && pip install dist/multimodal_ja-*-py3-none-any.whl \
  # Clean
  && rm ./dist/multimodal_ja-*-py3-none-any.whl ./poetry.lock ./pyproject.toml \
  && apt-get -y remove build-essential cmake curl file python$PYTHON_VERSION-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
RUN echo "" >> ~/.bashrc \
  && echo "alias jnl='jupyter notebook list'" >> ~/.bashrc \
  && echo "alias venv-activate='. /venv/bin/activate'" >> ~/.bashrc \
  && echo "alias jl='jupyter lab --no-browser --allow-root --ip=0.0.0.0 --port='" >> ~/.bashrc
