from fastapi import APIRouter
from modules.classes import LogList, LogInfo
from modules.database import add_log, list_logs

router = APIRouter()

@router.post("/add", response_model=LogInfo, tags=["logs"])
async def add_log_(log_info: LogInfo):
    add_log(log_info.unix_time, log_info.text)
    return log_info

@router.get("/view", response_model=LogList, tags=["logs"])
async def view_logs_():
    return list_logs(100)