FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y gcc \
    python3-pip \
    build-essential \
    cmake

RUN pip3 install --upgrade pip && \
    pip3 install flask==2.2.2 \
    redis==5.0.1 \
    Werkzeug==2.2.2 \
    requests==2.31.0 \
    numpy==1.21.6 \
    uwsgi==2.0.21 \
    faiss-cpu==1.7.4


WORKDIR /app

COPY . /app

EXPOSE ${SERVICE_PORT}

CMD uwsgi --http 0.0.0.0:${SERVICE_PORT} --master -w app:app