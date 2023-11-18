import redis

import sys


class Registry:
    def __init__(self, host: str, port: str, password: str, service_name: str, service_port: int):
        self.service_name = service_name
        self.service_port = service_port
        self._init_redis(host, port, password)

    def _init_redis(self, host, port, password) -> redis.Redis:
        self.redis = redis.Redis(
            host=host,
            port=port,
            password=password,
            decode_responses=True
        )

    def register(self, center: list):
        self.redis.hset(self.service_name, 'center', center)
        self.redis.hset(self.service_name, 'service_port', self.service_port)

    def unregister(self):
        self.redis.delete(self.service_name)

    def stop_service(self, sig, fra):
        self.unregister()
        sys.exit(0)
