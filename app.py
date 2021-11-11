from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from routers import schedulers, tasks, users, websockets

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pno3cwa1.student.cs.kuleuven.be",
        "http://localhost:5000",
        "http://localhost:11000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware)

app.include_router(schedulers.router, prefix="/api/scheduler")
app.include_router(tasks.router, prefix="/api/task")
app.include_router(users.router, prefix="/api/user")
app.include_router(websockets.router, prefix="/ws")