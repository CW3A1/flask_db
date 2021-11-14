from asyncio import Event, gather

from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse
from modules import database, environment
from orjson import dumps

router = APIRouter()

task_to_ws = dict()
async def sendMessageToPC(pc):
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

@router.get("/test")
async def get():
    return HTMLResponse(f"""<script>
var ws = new WebSocket("{environment.WS_URL}");
ws.onmessage = function(event) {{
    document.body.innerHTML = JSON.parse(event.data)["pc"] + "|" + JSON.parse(event.data)["status"]
}};
ws.onopen = () => ws.send("eeklo");
window.onbeforeunload = function() {{
    ws.onclose = function () {{}};
    ws.close();
}};
</script>""")
