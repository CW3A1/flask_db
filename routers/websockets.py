from asyncio import Event, gather

from fastapi import APIRouter, WebSocket
from modules import database
from orjson import dumps

router = APIRouter()

task_to_ws = dict()
async def broadcastMessage(pc):
    await gather(*[client.send_text(dumps(database.status_scheduler(pc)).decode("utf-8")) for client in task_to_ws[pc]])

@router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    pc = await websocket.receive_text()
    task_to_ws.setdefault(pc, set())
    task_to_ws[pc].add(websocket)
    await websocket.send_text(dumps(database.status_scheduler(pc)).decode("utf-8"))
    while True:
        await Event().wait()