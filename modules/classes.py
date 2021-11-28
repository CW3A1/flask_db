from typing import Dict, List

from pydantic import BaseModel

# Schedulers
class SchedulerInfo(BaseModel):
    pc: str
    status: int
    pc_domain: str

# Tasks
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

# Users
class User(BaseModel):
    email: str
    password: str

class UserToken(BaseModel):
    uuid: str
    jwt: str
