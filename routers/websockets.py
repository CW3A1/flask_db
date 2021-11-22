from asyncio import Event, gather

from fastapi import APIRouter, WebSocket
from modules import database
from orjson import dumps

router = APIRouter()

task_to_ws = dict()
async def broadcastMessage(task_id):
    await gather(*[client.send_text(dumps(database.status_task(task_id)).decode("utf-8")) for client in task_to_ws[task_id]])

@router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    task_id = await websocket.receive_text()
    task_to_ws.setdefault(task_id, set())
    task_to_ws[task_id].add(websocket)
    await websocket.send_text(dumps(database.status_task(task_id)).decode("utf-8"))
    while True:
        await Event().wait()