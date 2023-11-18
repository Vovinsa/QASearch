from flask import Flask, request, jsonify

import numpy as np
import faiss

import json
import signal

from utils import env, registry


center = np.load(
    f'/var/data/clusters/clusters_centers_use_dg{env.DATA_GENERATION}.pkl', allow_pickle=True
)[str(env.CLUSTER)]
center = ','.join([str(num) for num in center])

indexes = faiss.read_index(f'/var/data/indexes/indexes_dg{env.DATA_GENERATION}_cluster{env.CLUSTER}.faiss')
with open(f'/var/data/other/index_document_cluster{env.CLUSTER}.json') as f:
    index_document = json.load(f)
with open(f'/var/data/other/document_embedding_cluster{env.CLUSTER}.json') as f:
    document_embedding = json.load(f)

app = Flask(__name__)

service_registry = registry.Registry(
    host=env.REDIS_HOST,
    password=env.REDIS_PASSWORD,
    port=env.REDIS_PORT,
    service_name=env.SERVICE_NAME,
    service_port=env.SERVICE_PORT
)

service_registry.register(center=center)

signal.signal(signal.SIGINT, service_registry.stop_service)
signal.signal(signal.SIGTERM, service_registry.stop_service)


@app.route('/top_k', methods=['POST'])
def top_k():
    query_embedding = np.array(request.json['query_embedding']).reshape(1, -1)
    k = request.json['k']
    _, index = indexes.search(query_embedding.astype(np.float32), k)
    documents = [index_document[str(i)] for i in index.tolist()[0]]
    embeddings = [document_embedding[doc] for doc in documents]
    return jsonify(documents=documents, documents_embeddings=embeddings)
