import uuid
from asyncio import ensure_future
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from modules import auth, database, toolbox
from pydantic import BaseModel

from routers.websockets import broadcastMessage

router = APIRouter()

class TaskInput(BaseModel):
    operation: str = "diff"
    options: Dict = {"f": "sin(x)",
                    "a": 0,
                    "order": 1,}

class TaskOutput(BaseModel):
    task_id: str
    status: str = 0
    pc: str
    input_values: TaskInput
    result: Dict
    uuid: str

class TaskList(BaseModel):
    tasks: List[TaskOutput]
    uuid: str

class CompleteTask(BaseModel):
    task_id: str
    data: Dict

@router.post("/add", response_model=TaskOutput, tags=["tasks"])
async def add_task(task_data: TaskInput, identifier: str = Depends(auth.header_to_identifier)):
    task_id = str(uuid.uuid4())[:8]
    database.add_task(task_id, task_data.dict(), identifier)
    ensure_future(toolbox.next_task())
    return database.status_task(task_id)

@router.get("/status", response_model=TaskOutput, tags=["tasks"])
async def view_task_status(task_id: str, identifier: str = Depends(auth.header_to_identifier)):
    if database.task_exists(task_id):
        resp = database.status_task(task_id)
        if resp["uuid"] in {"", identifier}:
            return resp
        raise HTTPException(status_code=403)
    raise HTTPException(status_code=404)

@router.post("/complete", tags=["tasks"])
async def complete_task(res: CompleteTask):
    database.complete_task(res.task_id, res.data)
    database.change_scheduler_status(database.status_task(res.task_id)["pc"], 0)
    await broadcastMessage(res.task_id)
    resp = database.status_task(res.task_id)
    return resp
