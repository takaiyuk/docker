# docker build . -t takaiyuk/multimodal -f ./Dockerfile
# docker run -d --name ${CONTAIINER_NAME} -p 8888:8899 -v ${PWD}:/workspace/ takaiyuk/multimodal
# docker exec -it ${CONTAINER_ID} /bin/bash
# jupyter notebook list
FROM takaiyuk/ml-base:latest
ENV APP_HOME /workspace
WORKDIR $APP_HOME
COPY requirements.txt $APP_HOME
COPY setup.py $APP_HOME
RUN apt-get update -y \
    && apt-get install -y clang cmake g++ libopencv-dev \
    # fastText
    && pip install git+https://github.com/facebookresearch/fastText.git \
    # requirements.txt
    && cd $APP_HOME \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    # Clean
    && apt-get -y remove clang cmake g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
CMD jupyter lab \
    --no-browser \
    --ip=0.0.0.0 \
    --allow-root
