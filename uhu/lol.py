task_to_ws = dict()
import orjson
from modules import database


async def lol(x, pc):
    await x[pc].send_text(orjson.dumps(database.status_scheduler(pc).dict()).decode("utf-8"))
