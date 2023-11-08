FROM tensorflow/serving:2.14.0

RUN apt-get update

RUN apt-get install -y wget tar

RUN wget https://tfhub.dev/google/universal-sentence-encoder-large/5?tf-hub-format=compressed -O /models/use.tar.gz
RUN mkdir -p /models/use/1 && \
    tar xvf /models/use.tar.gz -C /models/use/1 && \
    rm /models/use.tar.gz

EXPOSE 8501

CMD ["tensorflow_model_server", "--rest_api_port=8501", "--model_base_path=/models/use", "--model_name=use"]