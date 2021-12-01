from asyncio import ensure_future
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from modules.auth import header_to_identifier
from modules.classes import CompleteTask, TaskInput, TaskOutput
from modules.database import (add_task, change_scheduler_status, complete_task,
                              status_task, task_exists)
from modules.toolbox import next_task

from routers.websockets import broadcastMessage

router = APIRouter()

@router.post("/add", response_model=TaskOutput, tags=["tasks"])
async def add_task_(task_data: TaskInput, identifier: str = Depends(header_to_identifier)):
    task_id = str(uuid4())[:8]
    add_task(task_id, task_data.dict(), identifier)
    ensure_future(next_task())
    return status_task(task_id)

@router.get("/status", response_model=TaskOutput, tags=["tasks"])
async def view_task_status_(task_id: str, identifier: str = Depends(header_to_identifier)):
    if task_exists(task_id):
        resp = status_task(task_id)
        if resp["uuid"] in {"", identifier}:
            return resp
        raise HTTPException(status_code=403)
    raise HTTPException(status_code=404)

@router.post("/complete", tags=["tasks"])
async def complete_task_(res: CompleteTask):
    complete_task(res.task_id, res.data)
    change_scheduler_status(status_task(res.task_id)["pc"], 0)
    await broadcastMessage(res.task_id)
    return status_task(res.task_id)
