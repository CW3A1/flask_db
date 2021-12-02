from asyncio import ensure_future
from time import time_ns

from requests import post

from modules.database import (add_log, change_scheduler_status, free_task,
                              oldest_pending_task, pending_task,
                              random_free_scheduler, status_scheduler,
                              status_task)

operation_paths = {
    "int": "/num_math/integration",
    "diff": "/num_math/differentiation",
    "opt": "/num_math/optimization",
    "lint": "/num_math/lagrange_interpolation",
    "taprox": "/num_math/taylor_approximation",
    "heateq": "/num_math/heat_equation",
    "symdiff": "/sym_math/sym_diff",
    "symint": "/sym_math/sym_int",
    "symlimit": "/sym_math/sym_limit",
    "symsolve": "/sym_math/sym_solver",
}

async def task(pc, task_id):
    status_task_, status_scheduler_ = status_task(task_id), status_scheduler(pc)
    operation, options = status_task_["input_values"]["operation"], status_task_["input_values"]["options"]
    options["task_id"] = status_task_["task_id"]
    try:
        post(status_scheduler_["pc_domain"] + operation_paths[operation], json=options)
        add_log(time_ns(), f"Successfully assigned task {task_id} to {pc}")
    except:
        free_task(task_id)
        change_scheduler_status(pc, 2)
        ensure_future(next_task())
        add_log(time_ns(), f"Failed to assign task {task_id} to {pc}")

async def next_task():
    randomFreeScheduler, oldestPendingTask = random_free_scheduler(), oldest_pending_task()
    if randomFreeScheduler and oldestPendingTask:
        add_log(time_ns(), f"Assigning task {oldestPendingTask} to {randomFreeScheduler}")
        pending_task(oldestPendingTask, randomFreeScheduler)
        change_scheduler_status(randomFreeScheduler, 1)
        await task(randomFreeScheduler, oldestPendingTask)
