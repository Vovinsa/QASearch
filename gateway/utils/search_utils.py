import numpy as np
from numpy import dot
from numpy.linalg import norm

from redis import Redis


def closest_cluster(query_embedding: np.ndarray, client: Redis) -> str:
    """
    Find the cluster with the closest centroid to a given query embedding.

    Parameters:
    - query_embedding (np.ndarray): The embedding vector of the query.
    - client (Redis): The Redis client used for retrieving cluster information.

    Returns:
    - str: The URL representing the cluster with the closest centroid to the query embedding.
    """
    service_keys = client.keys()

    indexes_url = ''

    max_sim = -np.inf

    for key in service_keys:
        res = client.hgetall(key)

        center = res['center']
        center = np.array([float(x) for x in center.split(',')])

        port = res['service_port']

        sim = similarity(query_embedding, center)

        if sim > max_sim:
            indexes_url = f'{key}:{port}/top_k'

    return indexes_url


def similarity(a: np.ndarray, b: np.ndarray) -> np.float32:
    """
    Calculate the cosine similarity between two vectors.

    Parameters:
    - a (np.ndarray): The first input vector.
    - b (np.ndarray): The second input vector.

    Returns:
    - np.float32: The cosine similarity between vectors 'a' and 'b', represented as a 32-bit floating-point number.
    """
    return (dot(a, b) / (norm(a) * norm(b))).astype(np.float32)
