import requests

from modules import database


async def task(pc, task_id):
    status_task = database.status_task(task_id)
    status_scheduler = database.status_scheduler(pc)
    operation = status_task["input_values"]["operation"]
    options = status_task["input_values"]["options"]
    options["task_id"] = status_task["task_id"]
    if operation == "int":
        requests.post(status_scheduler["pc_domain"] + "/num_math/integration", json=options)
    if operation == "diff":
        requests.post(status_scheduler["pc_domain"] + "/num_math/differentiation", json=options)
    if operation == "opt":
        requests.post(status_scheduler["pc_domain"] + "/num_math/optimization", json=options)
    if operation == "lint":
        requests.post(status_scheduler["pc_domain"] + "/num_math/lagrange_interpolation", json=options)
    if operation == "taprox":
        requests.post(status_scheduler["pc_domain"] + "/num_math/taylor_approximation", json=options)
    if operation == "heateq":
        requests.post(status_scheduler["pc_domain"] + "/num_math/heat_equation", json=options)

async def next_task():
    randomFreeScheduler = database.random_free_scheduler()
    oldestPendingTask = database.oldest_pending_task()
    if randomFreeScheduler and oldestPendingTask:
        database.pending_task(oldestPendingTask, randomFreeScheduler)
        database.change_scheduler_status(randomFreeScheduler, 1)
        await task(randomFreeScheduler, oldestPendingTask)
