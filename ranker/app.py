from flask import Flask, jsonify, request

import onnxruntime as ort
import numpy as np


app = Flask(__name__)

model = ort.InferenceSession('models/knrm.onnx')


@app.route('/rank', methods=['POST'])
def rank():
    """
    Endpoint for ranking documents based on a query embedding.

    Parameters:
    - query_embedding (list): The embedding vector for the query.
    - documents_embeddings (list): List of embedding vectors for documents.
    - documents (list): List of documents corresponding to the embeddings.

    Return:
    - JSON object containing 'ranked_documents': List of documents ranked based on the model prediction.

    Example:
        POST /rank
        {
            "query_embedding": [0.1, 0.2, ..., 0.5],
            "documents_embeddings": [[0.2, 0.3, ..., 0.7], [0.4, 0.1, ..., 0.9], ...],
            "documents": ["Document 1", "Document 2", ...]
        }

    Note:
    - The input embeddings and documents must be of the same length.
    - The embedding vectors should have a shape of (512,) for each element.
    - The model used for prediction is assumed to be globally defined.
    """
    query_embedding = request.json['query_embedding']
    documents_embeddings = request.json['documents_embeddings']
    documents = request.json['documents']

    query_embedding = [query_embedding for _ in range(len(documents_embeddings))]

    query_embedding = np.array(query_embedding).reshape((-1, 1, 512))
    documents_embeddings = np.array(documents_embeddings).reshape((-1, 1, 512))

    inp = {'query': query_embedding.astype(np.float32), 'document': documents_embeddings.astype(np.float32)}
    prediction = model.run(None, inp)[0]

    ranked_indexes = (-prediction).argsort()

    ranked_documents = np.array(documents)[ranked_indexes].reshape(-1).tolist()

    return jsonify({'ranked_documents': ranked_documents})
