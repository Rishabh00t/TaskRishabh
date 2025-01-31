from fastapi import FastAPI
from src.resource.user.api import user_router
from src.resource.task.api import task_router

app = FastAPI(
    title="Role-Based To-Do List API",
    description="""
    This API allows users to manage a to-do list with role-based access control (RBAC). 
    Users can create, read, update, and delete tasks, while administrators have additional 
    privileges for managing user roles and tasks. 
    
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/", summary="Welcome endpoint")
def read_app():
    """
    The welcome endpoint provides a simple greeting message for the API.
    It indicates that the API is a role-based to-do list system that supports users and admins.
    """
    return {"message": "Welcome to the Role-Based To-Do List API using FastAPI - Created by Rishabh"}

# Include routers for user and task management
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(task_router, prefix="/tasks", tags=["Tasks"])
