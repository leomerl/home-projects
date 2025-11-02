import redis
from app.config import REDIS_HOST, REDIS_PORT

rbin = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=False)

rtext = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def redis_ping() -> bool:
    try:
        rbin.ping()
        return True
    except Exception:
        return False