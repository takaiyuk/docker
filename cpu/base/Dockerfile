# ./build.sh
# ref.) https://future-architect.github.io/articles/20200513/
FROM python:3.8.3-buster as builder
ENV APP_HOME /workspace
WORKDIR $APP_HOME
COPY requirements.txt $APP_HOME
RUN apt-get -y update \
  && apt-get -y install clang cmake nodejs npm \
  && git clone --recursive https://github.com/microsoft/LightGBM && cd LightGBM && mkdir build && cd build && cmake .. && make -j4 && cd ../python-package && python setup.py install && cd ../.. && rm -r LightGBM \
  && git clone https://github.com/pfnet-research/xfeat.git && cd xfeat && python setup.py install && cd .. && rm -r xfeat \
  && pip install -r requirements.txt \
  && export NODE_OPTIONS=--max-old-space-size=4096 \
  && jupyter labextension install @jupyterlab/toc \
  && jupyter labextension install jupyterlab-plotly@4.7.1 \
  && jupyter nbextension enable --py widgetsnbextension

FROM python:3.8.3-slim-buster as runner
ENV APP_HOME /workspace
WORKDIR $APP_HOME
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/share/jupyter /usr/local/share/jupyter
COPY --from=builder /usr/lib/x86_64-linux-gnu/libgomp.so.1 /usr/lib/x86_64-linux-gnu/libgomp.so.1
RUN apt-get -y update \
  && apt-get -y install curl git unzip vim wget \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && mkdir /root/.kaggle
