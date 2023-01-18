from functools import lru_cache

from redis import Redis
from config import config


class RedisService:
    def __init__(self):
        self._redis: Redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)

    def set_review(self, review_uuid: str, class_result: str):
        self._redis.set(review_uuid, class_result)


@lru_cache
def get_redis_service() -> RedisService:
    return RedisService()
