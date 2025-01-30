from fastapi import APIRouter,HTTPException,Depends,Security
from sqlalchemy.orm import Session
from src.resource.task.schema import Tasks_schema,Update_task_schema
from src.functionallity.task import create_task,get_task,update_task,delete_task
from database.database import get_db
from fastapi.security import HTTPBearer

security = HTTPBearer()

task_router = APIRouter(tags=['CURD Task by User'])

@task_router.post("/create_task")
def create_user_task(task:Tasks_schema,db:Session=Depends(get_db),token:str=Security(security)):
    try:
        response = create_task(task=task,db=db,token=token)
        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@task_router.get("/get_task")
def get_task_by_id(owner_id:int,db:Session=Depends(get_db)):
    try:
        response = get_task(owner_id,db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@task_router.patch("/update_task")
def update_user_task(task:Update_task_schema,db:Session=Depends(get_db)):
    try:
        response = update_task(task,db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@task_router.delete("/delete_task")
def delete_user_task(task_id:int,db:Session=Depends(get_db)):
    try:
        response = delete_task(task_id,db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))