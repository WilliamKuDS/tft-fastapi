from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials
import time
from functools import wraps
from typing import Optional

from app.utils.rate_limiter.memory_client import InMemoryRateLimiter
from app.utils.rate_limiter.utils import generate_key, parse_refill_rate
from app.utils.auth.auth_supabase import verify_token, get_user_tier
from app.utils.rate_limiter.redis_client import RedisClient


class RateLimiter:
    def __init__(self, default_bucket_limit: int = 0, default_refill_rate: str = None, backend: str = "memory"):
        self.default_bucket_limit = default_bucket_limit
        self.default_refill_rate = default_refill_rate
        if backend == 'memory':
            self.backend = backend
            self.memory_limiter = InMemoryRateLimiter()
        elif backend == 'redis':
            self.backend = backend
            self.redis_client = RedisClient()
        else:
            raise ValueError(f"Unsupported backend: {backend}. Supported backends are 'redis' and 'memory'.")

    def get_rate_limit(self, tier: int, custom_limits: dict):
        bucket_size, refill_rate_str = custom_limits.get(tier, (
            self.default_bucket_limit, self.default_refill_rate))
        if bucket_size == 0:
            return bucket_size, refill_rate_str
        refill_rate = parse_refill_rate(refill_rate_str)
        return bucket_size, refill_rate

    async def check_rate_limit(self, key: str, limit: int, refill_rate: float):
        current_time = int(time.time() * 1000)
        if self.backend == "redis":
            redis_instance = await self.redis_client.get_instance()
            lua_sha = await self.redis_client.get_lua_sha()
            try:
                tokens, wait_time = await redis_instance.evalsha(lua_sha, 1, key, limit, refill_rate, current_time)
                return float(tokens), int(wait_time)
            except Exception as e:
                print(f"Error during Redis evalsha: {e}")
                raise e

        elif self.backend == "memory":
            tokens, wait_time = await self.memory_limiter.check_rate_limit(key, limit, refill_rate, current_time)
            return float(tokens), int(wait_time)

    def tier_limit(self, tier_limits: dict = None):
        if tier_limits is None:
            tier_limits = {}

        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                request: Request = kwargs.get('request')
                if not request:
                    raise HTTPException(status_code=500, detail="Request object not found")

                token: Optional[HTTPAuthorizationCredentials] = kwargs.get('token')

                ip = request.client.host
                route_key = request.url.path

                if token:
                    user_id = await verify_token(token.credentials)
                    if user_id:
                        tier = await get_user_tier(user_id)
                    else:
                        user_id = "anonymous"
                        tier = 0  # Default to lowest tier if token is invalid
                else:
                    user_id = "anonymous"
                    tier = 0  # Default to lowest tier if no token provided

                limit, refill_rate = self.get_rate_limit(tier, tier_limits)
                if limit == 0:
                    raise HTTPException(status_code=403, detail="Forbidden")

                key = generate_key(ip, user_id, route_key)

                tokens, wait_time = await self.check_rate_limit(key, limit, refill_rate)

                if tokens < 1:
                    raise HTTPException(status_code=429,
                                        detail=f"Rate limit exceeded. Try again in {wait_time / 1000} seconds.")

                return await func(*args, **kwargs)

            return wrapper

        return decorator

    def limit(self, bucket_limit: int = 0, refill_rate_str: str = None):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                request: Request = kwargs.get('request')
                if not request:
                    raise HTTPException(status_code=500, detail="Request object not found")

                if bucket_limit == 0:
                    raise HTTPException(status_code=403, detail="Forbidden")

                token: Optional[HTTPAuthorizationCredentials] = kwargs.get('token')

                ip = request.client.host
                route_key = request.url.path

                if token:
                    user_id = await verify_token(token.credentials)
                else:
                    user_id = "anonymous"

                refill_rate = parse_refill_rate(refill_rate_str)
                key = generate_key(ip, user_id, route_key)

                tokens, wait_time = await self.check_rate_limit(key, bucket_limit, refill_rate)

                if tokens < 1:
                    raise HTTPException(status_code=429,
                                        detail=f"Rate limit exceeded. Try again in {wait_time / 1000} seconds.")

                return await func(*args, **kwargs)

            return wrapper

        return decorator
