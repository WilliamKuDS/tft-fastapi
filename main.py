from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.routes.tft import update_api
from app.routes.tft import account_api, summoner_api, league_api, summoner_league_api, region_api
from app.routes.tft import set_api, patch_api, companion_api
from app.routes.tft import match_api, match_summoner_api

app = FastAPI()

# CORS settings
origins = [
    "http://localhost:3000",
    # Add other origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"TFT API Running"}


# TFT API Routes
app.include_router(update_api.router, tags=["update"])
app.include_router(account_api.router, tags=["account"])
app.include_router(summoner_api.router, tags=["summoner"])
app.include_router(league_api.router, tags=["league"])
app.include_router(region_api.router, tags=["region"])
app.include_router(summoner_league_api.router, tags=["summoner league"])
app.include_router(set_api.router, tags=["set"])
app.include_router(patch_api.router, tags=["patch"])
app.include_router(companion_api.router, tags=["companion"])
app.include_router(match_api.router, tags=["match"])
app.include_router(match_summoner_api.router, tags=["match summoner"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, ssl_keyfile="path/to/key.pem", ssl_certfile="path/to/cert.pem")
