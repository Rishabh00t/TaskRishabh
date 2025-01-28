from fastapi import FastAPI
from src.resource.user.api import user_router
from src.resource.task.api import task_router
app = FastAPI()

@app.get("/")
def read_app():
    return {"welcome to the Role-Based To-Do List API using FastAPI"}

app.include_router(user_router)
app.include_router(task_router)