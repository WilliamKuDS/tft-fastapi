import hashlib
import re


def generate_key(ip: str, user_id: str, route: str):
    combined = f"{ip}:{user_id}:{route}"
    return hashlib.md5(combined.encode()).hexdigest()


def parse_refill_rate(refill_rate: str) -> float:
    if refill_rate is None:
        return 0.0
    match = re.match(r"(\d+)/(\w+)", refill_rate)
    if not match:
        raise ValueError("Invalid refill rate format. Use 'number/unit' format.")
    rate = int(match.group(1))
    unit = match.group(2)

    if unit == "second" or unit == "seconds":
        return rate / 1000  # tokens per millisecond
    elif unit == "minute" or unit == "minutes":
        return rate / (60 * 1000)  # tokens per millisecond
    elif unit == "hour" or unit == "hours":
        return rate / (60 * 60 * 1000)  # tokens per millisecond
    else:
        raise ValueError("Unsupported time unit. Use 'second(s)', 'minute(s)', or 'hour(s)'.")
