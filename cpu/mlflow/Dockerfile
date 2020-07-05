FROM python:3.7.7-slim
ENV APP_HOME /workspace
WORKDIR $APP_HOME
RUN pip install mlflow==1.7.2
CMD mlflow ui \
  --port=5000 \
  --host=0.0.0.0
