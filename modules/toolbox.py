import requests

from modules import database, environment


async def task(pc, task_id):
    input_values = database.status_task(task_id)["input_values"]
    res = requests.post(environment.WORKER_URL + "/num_math/differentiation", timeout=3, json=input_values).json()
    database.complete_task(task_id, res)
    database.change_scheduler_status(pc, 0)

async def next_task():
    randomFreeScheduler = database.random_free_scheduler()
    oldestPendingTask = database.oldest_pending_task()
    if randomFreeScheduler and oldestPendingTask:
        database.pending_task(oldestPendingTask, randomFreeScheduler)
        await database.change_scheduler_status(randomFreeScheduler, 1)
        await task(randomFreeScheduler, oldestPendingTask)
