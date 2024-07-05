from fastapi import HTTPException, Request
from dotenv import load_dotenv
import os

load_dotenv()

allowed_ips = os.getenv("ALLOWED_IPS", "").split(",")


def check_ip(request: Request):
    client_ip = request.client.host
    if client_ip not in allowed_ips:
        raise HTTPException(status_code=403, detail="Access forbidden: Your IP is not allowed")
    return True
