# from slowapi import Limiter
# from slowapi.util import get_remote_address
# from dotenv import load_dotenv
# import os

from app.utils.rate_limiter.main import RateLimiter

# load_dotenv()
#
# redis_host = os.environ.get('REDIS_HOST', '127.0.0.1')
# redis_port = os.environ.get('REDIS_PORT', 6379)
# redis_db = os.environ.get('REDIS_DB', 'redis')

# SlowAPI
# limiter = Limiter(key_func=get_remote_address, storage_uri=f"redis://{redis_host}:{redis_port}/{redis_db}")

# Custom RateLimiter
limiter = RateLimiter(
    backend='redis'
)
