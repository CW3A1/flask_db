import requests

from modules import database


async def task(pc, task_id):
    status_task = database.status_task(task_id)
    status_scheduler = database.status_scheduler(pc)
    operation = status_task["input_values"]["operation"]
    if operation == "int":
        res = requests.post(status_scheduler["pc_domain"] + "/num_math/integration", timeout=3, json=status_task["input_values"]["options"]).json()
    if operation == "diff":
        res = requests.post(status_scheduler["pc_domain"] + "/num_math/differentiation", timeout=3, json=status_task["input_values"]["options"]).json()
    if operation == "opt":
        res = requests.post(status_scheduler["pc_domain"] + "/num_math/optimization", timeout=3, json=status_task["input_values"]["options"]).json()
    if operation == "lint":
        res = requests.post(status_scheduler["pc_domain"] + "/num_math/lagrange_interpolation", timeout=3, json=status_task["input_values"]["options"]).json()
    if operation == "taprox":
        res = requests.post(status_scheduler["pc_domain"] + "/num_math/taylor_approximation", timeout=3, json=status_task["input_values"]["options"]).json()
    if operation == "heateq":
        res = requests.post(status_scheduler["pc_domain"] + "/num_math/heat_equation", timeout=3, json=status_task["input_values"]["options"]).json()
    database.complete_task(task_id, res)
    database.change_scheduler_status(pc, 0)

async def next_task():
    randomFreeScheduler = database.random_free_scheduler()
    oldestPendingTask = database.oldest_pending_task()
    if randomFreeScheduler and oldestPendingTask:
        database.pending_task(oldestPendingTask, randomFreeScheduler)
        await database.change_scheduler_status(randomFreeScheduler, 1)
        await task(randomFreeScheduler, oldestPendingTask)
