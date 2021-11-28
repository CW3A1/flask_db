from requests import post

from modules.database import (change_scheduler_status, oldest_pending_task,
                              pending_task, random_free_scheduler,
                              status_scheduler, status_task)

operation_paths = {
    "int": "/num_math/integration",
    "diff": "/num_math/differentiation",
    "opt": "/num_math/optimization",
    "lint": "/num_math/lagrange_interpolation",
    "taprox": "/num_math/taylor_approximation",
    "heateq": "/num_math/heat_equation",
}

async def task(pc, task_id):
    status_task_, status_scheduler_ = status_task(task_id), status_scheduler(pc)
    operation, options = status_task_["input_values"]["operation"], status_task_["input_values"]["options"]
    options["task_id"] = status_task_["task_id"]
    post(status_scheduler_["pc_domain"] + operation_paths[operation], json=options)

async def next_task():
    randomFreeScheduler, oldestPendingTask = random_free_scheduler(), oldest_pending_task()
    if randomFreeScheduler and oldestPendingTask:
        pending_task(oldestPendingTask, randomFreeScheduler)
        change_scheduler_status(randomFreeScheduler, 1)
        await task(randomFreeScheduler, oldestPendingTask)
