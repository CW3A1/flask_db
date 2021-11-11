from asyncio import Event

from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse
from modules import database, environment
from uhu.lol import task_to_ws, lol

router = APIRouter()

@router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    pc = await websocket.receive_text()
    task_to_ws[pc] = websocket
    await lol(task_to_ws, pc)
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
