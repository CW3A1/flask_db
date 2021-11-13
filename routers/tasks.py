import uuid
from typing import Dict, List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from modules import auth, database, toolbox
from pydantic import BaseModel

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

@router.post("/add", response_model=TaskOutput, tags=["tasks"])
async def add_task(task_data: TaskInput, background: BackgroundTasks, identifier: str = Depends(auth.header_to_identifier)):
    task_id = str(uuid.uuid4())[:8]
    database.add_task(task_id, task_data.dict(), identifier)
    background.add_task(toolbox.next_task)
    return database.status_task(task_id)

@router.get("/status", response_model=TaskOutput, tags=["tasks"])
async def view_task_status(task_id: str, identifier: str = Depends(auth.header_to_identifier)):
    if database.task_exists(task_id):
        resp = database.status_task(task_id)
        if resp["uuid"] in {"", identifier}:
            return resp
        raise HTTPException(status_code=403)
    raise HTTPException(status_code=404)
