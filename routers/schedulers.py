from fastapi import APIRouter, HTTPException
from modules import database, environment
from pydantic import BaseModel

router = APIRouter()

class SchedulerInfo(BaseModel):
    pc: str
    status: int = 0

@router.put("/status", response_model=SchedulerInfo, tags=["schedulers"])
async def change_scheduler_status(new_info: SchedulerInfo, auth: str):
    if auth == environment.AUTH_SECRET:
        if database.scheduler_exists(new_info.pc):
            if new_info.status in (0, 1, 2):
                await database.change_scheduler_status(new_info.pc, new_info.status)
                return database.status_scheduler(new_info.pc)
            raise HTTPException(status_code=403)
        raise HTTPException(status_code=404)
    raise HTTPException(status_code=401)

@router.get("/status", response_model=SchedulerInfo, tags=["schedulers"])
async def view_scheduler_status(pc: str):
    if database.scheduler_exists(pc):
        return database.status_scheduler(pc)
    raise HTTPException(status_code=404)
