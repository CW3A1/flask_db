from fastapi import APIRouter, HTTPException
from modules.classes import SchedulerInfo
from modules.database import (change_scheduler_status, scheduler_exists,
                              status_scheduler)
from modules.environment import AUTH_SECRET

router = APIRouter()

@router.put("/status", response_model=SchedulerInfo, tags=["schedulers"])
async def change_scheduler_status_(new_info: SchedulerInfo, auth: str):
    if auth == AUTH_SECRET:
        if scheduler_exists(new_info.pc):
            if new_info.status in (0, 1, 2):
                await change_scheduler_status(new_info.pc, new_info.status)
                return status_scheduler(new_info.pc)
            raise HTTPException(status_code=403)
        raise HTTPException(status_code=404)
    raise HTTPException(status_code=401)

@router.get("/status", response_model=SchedulerInfo, tags=["schedulers"])
async def view_scheduler_status_(pc: str):
    if scheduler_exists(pc):
        return status_scheduler(pc)
    raise HTTPException(status_code=404)
