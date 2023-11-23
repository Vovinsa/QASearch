import pytest

import numpy as np

import os

from gateway.utils.search_utils import closest_cluster
from gateway.utils.registry import Registry


def test_closest_cluster():
    REDIS_TEST_HOST = os.environ['REDIS_TEST_HOST']
    REDIS_TEST_PORT = os.environ['REDIS_TEST_PORT']
    REDIS_TEST_PASSWORD = os.environ['REDIS_TEST_PASSWORD']

    registry = Registry(
        host=REDIS_TEST_HOST,
        port=REDIS_TEST_PORT,
        password=REDIS_TEST_PASSWORD
    )

    registry.redis.hset('service_cluster0_dg1', 'center', '-0.01651316,0.015409566,0.024219709,0.01774026,0.01663145,0.023400806,0.016130716')
    registry.redis.hset('service_cluster0_dg1', 'service_port', 8002)

    registry.redis.hset('service_cluster1_dg1', 'center', '-0.01836138,0.02587711,0.012265775,0.011129407,-0.04124325,0.020997923,0.009999914')
    registry.redis.hset('service_cluster1_dg1', 'service_port', 8003)

    registry.redis.hset('service_cluster2_dg1', 'center', '-0.033685625,0.014448523,0.00896315,0.005386063,0.021105986,0.035004504,0.00421367')
    registry.redis.hset('service_cluster2_dg1', 'service_port', 8004)

    registry.redis.hset('service_cluster3_dg1', 'center', '-0.023187941,0.0065219766,0.008612059,0.0029294165,-0.074019805,0.014411052,-0.0019801888')
    registry.redis.hset('service_cluster3_dg1', 'service_port', 8005)

    query_embedding = np.array([-0.03411436, 0.00789111, 0.14921543, 0.07004186, 0.05643401, -0.11981615, 0.15191882])

    assert closest_cluster(query_embedding, registry.redis) == 'http://service_cluster0_dg1:8002/top_k'
