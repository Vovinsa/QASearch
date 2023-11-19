from flask import Flask, jsonify, request

from utils import env, registry, search_utils

import numpy as np
import requests


app = Flask(__name__)

service_registry = registry.Registry(
    host=env.REDIS_HOST,
    port=env.REDIS_PORT,
    password=env.REDIS_PASSWORD
)


@app.route('/search', methods=['POST'])
def search():
    """
    Endpoint for handling search requests.

    Parameters:
    - query (str): The search query.
    - k (int): The number of top results to retrieve.

    Returns:
    - Response: JSON response containing the ranked documents.

    Example:
        POST /search
        {
            "query": "Example query",
            "k": 5
        }

    Note:
    - The 'embedder' service is expected to be running and accessible at 'embedder:8501'.
    - The 'search_utils.closest_cluster' function is used to find the closest cluster in the service registry.
    - The identified cluster is queried for documents and their embeddings.
    - The 'ranker' service at 'ranker:8001' is used to rank the documents based on the query embedding.
    - The response contains a JSON object with 'ranked_documents' representing the top-ranked results.
    """
    query = request.json['query']
    k = request.json['k']

    query_embedding = requests.post(
        'embedder:8501/v1/models/use:predict', json={'instances': [query]}
    ).json()['predictions'][0]

    indexes_url = search_utils.closest_cluster(np.array(query_embedding), service_registry.redis)

    documents = requests.post(indexes_url, json={'query_embedding': query_embedding, 'k': k}).json()['documents']
    documents_embeddings = requests.post(
        'embedder:8501/v1/models/use:predict', json={'instances': documents}
    ).json()['predictions']

    ranked_documents = requests.post(
        'ranker:8001/rank',
        json={'query_embedding': query_embedding, 'documents_embeddings': documents_embeddings, 'documents': documents}
    ).json()['ranked_documents']

    return jsonify(ranked_documents=ranked_documents)
