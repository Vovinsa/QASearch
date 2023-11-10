FROM python:3.8-slim

RUN apt-get update && apt-get install -y python3-pip \
    gcc

RUN pip3 install --upgrade pip && \
    pip3 install flask==2.2.2 \
    requests==2.31.0 \
    uwsgi==2.0.21 \
    Werkzeug==2.2.2 \
    onnxruntime==1.15.0

WORKDIR /app

COPY . /app

EXPOSE 8001

CMD uwsgi --ini ranker_uwsgi.ini