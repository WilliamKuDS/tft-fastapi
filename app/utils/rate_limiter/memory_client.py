import asyncio
from collections import defaultdict


class InMemoryRateLimiter:
    def __init__(self):
        self.buckets = defaultdict(lambda: {"tokens": 0.0, "last_refreshed": 0})
        self.locks = defaultdict(asyncio.Lock)

    async def check_rate_limit(self, key: str, limit: int, refill_rate: float, current_time: int):
        async with self.locks[key]:
            bucket = self.buckets[key]

            tokens = bucket["tokens"]
            last_refreshed = bucket["last_refreshed"]

            elapsed_ms = current_time - last_refreshed
            tokens_to_add = elapsed_ms * refill_rate
            tokens = min(float(limit), float(tokens + tokens_to_add))

            if tokens >= 1:
                tokens -= 1
                self.buckets[key]["tokens"] = tokens
                if tokens == 0:
                    time_to_next_token = (1 - tokens) / refill_rate
                    self.buckets[key]["last_refreshed"] = current_time
                    return tokens + 1, int(time_to_next_token)
                else:
                    self.buckets[key]["last_refreshed"] = current_time
                    return tokens + 1, 0
            else:
                time_to_next_token = (1 - tokens) / refill_rate
                self.buckets[key]["tokens"] = tokens
                self.buckets[key]["last_refreshed"] = current_time
                return tokens, int(time_to_next_token)
