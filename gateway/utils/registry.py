import redis


class Registry:
    def __init__(self, host: str, port: str, password: str):
        self._init_redis(host, port, password)

    def _init_redis(self, host, port, password) -> redis.Redis:
        self.redis = redis.Redis(
            host=host,
            port=port,
            password=password,
            decode_responses=True
        )
