from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import HTMLResponse
from modules import environment

router = APIRouter()

@router.websocket("")
async def websocket_endpoint(websocket: WebSocket, request: Request):
    await websocket.accept()
    pc = await websocket.receive_text()
    request.app.task_to_ws[pc] = websocket

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
