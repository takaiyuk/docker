FROM takaiyuk/ml-base-gpu:latest
ENV APP_HOME /workspace
ENV TZ Asia/Tokyo
WORKDIR $APP_HOME
# COPY requirements.txt $APP_HOME
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime \
  # && apt-get update -y \
  # && apt-get install -y --no-install-recommends HOGE \
  # && . /venv/bin/activate \
  # && pip install -r requirements.txt \
  # && apt-get remove -y HOGE \
  # && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
# set alias
RUN echo "" >> ~/.bashrc \
  && echo "alias jnl='jupyter notebook list'" >> ~/.bashrc \
  && echo "alias venv-activate='. /venv/bin/activate'" >> ~/.bashrc \
  && echo "alias jl='jupyter lab --no-browser --allow-root --ip=0.0.0.0 --port='" >> ~/.bashrc
