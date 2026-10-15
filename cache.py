
import os
import redis

def get_client():
    return redis.Redis.from_url(
        os.environ["REDIS_URL"],
        decode_responses=True
    )

def get_cached_visits():
    value = get_client().get("total_visits")
    return int(value) if value is not None else None

def set_cached_visits(count):
    get_client().set("total_visits", count, ex=60)

def clear_cached_visits():
    get_client().delete("total_visits")
