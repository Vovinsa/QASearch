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
    """
    Endpoint for retrieving the top-k documents based on a query embedding.

    Parameters:
    - query_embedding (list): The embedding vector for the query.
    - k (int): The number of top results to retrieve.

    Returns:
    - Response: JSON response containing the top-k documents and their embeddings.

    Example:
        POST /top_k
        {
            "query_embedding": [0.1, 0.2, ..., 0.5],
            "k": 5
        }

    Note:
    - The query_embedding is expected to be a list representing the embedding vector for the query.
    - The 'k' parameter specifies the number of top results to retrieve.
    - The 'indexes' object is used to search for the top-k documents based on the query embedding.
    - The response contains a JSON object with 'documents' representing the top-k document IDs.
    """
    query_embedding = np.array(request.json['query_embedding']).reshape(1, -1)
    k = request.json['k']
    _, index = indexes.search(query_embedding.astype(np.float32), k)
    documents = [index_document[str(i)] for i in index.tolist()[0]]
    return jsonify(documents=documents)
