import pytest

import requests
import os


def test_right_query():
    APP_HOST = os.environ['APP_HOST']
    APP_PORT = os.environ['APP_PORT']

    response = requests.post(f'http://{APP_HOST}:{APP_PORT}/search', json={'query': 'How are you?', 'k': 5})

    assert response.status_code == 200
    assert len(response.json()['ranked_documents']) == 5


def test_wrong_query():
    APP_HOST = os.environ['APP_HOST']
    APP_PORT = os.environ['APP_PORT']

    response = requests.post(f'http://{APP_HOST}:{APP_PORT}/search', json={'query': 0, 'k': 5})

    assert response.status_code == 500
