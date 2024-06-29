from fastapi import FastAPI
import uvicorn
from app.routes.tft import set_api, patch_api, update_api
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# TFT API Routes
app.include_router(set_api.router, tags=["set"])
app.include_router(patch_api.router, tags=["patch"])
app.include_router(update_api.router, tags=["update"])

@app.get("/")
async def root():
    return {"TFT Database"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, ssl_keyfile="path/to/key.pem", ssl_certfile="path/to/cert.pem")