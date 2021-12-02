from asyncio import Event, gather

from fastapi import APIRouter, WebSocket
from modules.database import status_task, udumps

router = APIRouter()

task_to_ws = dict()
async def broadcastMessage(task_id):
    if task_id in task_to_ws:
        await gather(*[client.send_text(udumps(status_task(task_id))) for client in task_to_ws[task_id]])

@router.websocket("")
async def websocket_endpoint_(websocket: WebSocket):
    await websocket.accept()
    task_id = await websocket.receive_text()
    task_to_ws.setdefault(task_id, set())
    task_to_ws[task_id].add(websocket)
    await websocket.send_text(udumps(status_task(task_id)))
    while True:
        await Event().wait()
