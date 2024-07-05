from redis import asyncio as aioredis
from dotenv import load_dotenv
import os

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")


class RedisClient:
    _instance = None
    _lua_sha = None

    @classmethod
    async def get_instance(cls):
        if cls._instance is None:
            cls._instance = await aioredis.from_url(
                f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
                decode_responses=True
            )
            await cls.load_lua_script()
        return cls._instance

    @classmethod
    async def close_instance(cls):
        if cls._instance:
            await cls._instance.close()
            cls._instance = None

    @classmethod
    async def load_lua_script(cls):
        lua_script = """
            local key = KEYS[1]
            local limit = tonumber(ARGV[1])
            local refill_rate = tonumber(ARGV[2])
            local current_time = tonumber(ARGV[3])

            -- Get or initialize the tokens and the last refreshed time
            local tokens = tonumber(redis.call('HGET', key, 'tokens') or limit)
            local last_refreshed = tonumber(redis.call('HGET', key, 'last_refreshed') or current_time)

            -- Calculate elapsed time and add tokens based on refill rate
            local elapsed_ms = current_time - last_refreshed
            local tokens_to_add = elapsed_ms * refill_rate

            tokens = math.min(limit, tokens + tokens_to_add)

            -- Update last_refreshed time
            redis.call('HSET', key, 'last_refreshed', current_time)

            -- Check if there are enough tokens available
            if tokens >= 1 then
                tokens = tokens - 1
                redis.call('HSET', key, 'tokens', tokens)
                local time_to_next_token = 0
                if tokens == 0 then
                    time_to_next_token = math.ceil(1 / refill_rate)
                end
                return {tokens + 1, time_to_next_token}
            else
                -- Calculate the time until 1 full token is available in milliseconds
                local time_to_next_token = math.ceil((1 - tokens) / refill_rate)
                redis.call('HSET', key, 'tokens', tokens)
                return {tokens, time_to_next_token}
            end
        """
        cls._lua_sha = await cls._instance.script_load(lua_script)
        if not cls._lua_sha:
            raise ValueError("Failed to load Lua script")

    @classmethod
    async def get_lua_sha(cls):
        if cls._lua_sha is None:
            await cls.load_lua_script()
        return cls._lua_sha
