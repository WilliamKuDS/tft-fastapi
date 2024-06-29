from fastapi import APIRouter, BackgroundTasks, Request, Depends
from sqlmodel import Session
from app.database.database import engine
from app.database.tft.update_tft import fetch_and_process_tft_data
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


def get_session():
    with Session(engine) as session:
        yield session



@router.post("/tft/update")
@limiter.limit("1/hour")
async def update_data(request: Request, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    background_tasks.add_task(fetch_and_process_tft_data, session)
    return {"message": "Starting TFT Database Update"}
