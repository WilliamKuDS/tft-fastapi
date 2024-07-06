from fastapi import APIRouter, BackgroundTasks, Request, Depends
from sqlmodel import Session
from app.database.tft.update_tft import fetch_and_process_tft_data
from app.routes.limiter import limiter
from app.routes.session import get_session

router = APIRouter()


@router.post("/tft/update")
@limiter.limit(1, "1/hour")
async def update_data(
        request: Request,
        background_tasks: BackgroundTasks,
        session: Session = Depends(get_session)
):
    background_tasks.add_task(fetch_and_process_tft_data, session)
    return {"message": "Starting TFT Database Update"}
