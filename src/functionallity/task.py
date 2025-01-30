from fastapi import Depends,HTTPException,Security
from database.database import get_db
from sqlalchemy.orm import Session
from src.resource.task.model import Task_model
from src.resource.task.schema import Tasks_schema,Update_task_schema
from fastapi.security import HTTPBearer
from src.utils.utils import verify_token

security = HTTPBearer()

def create_task(task:Tasks_schema,
                db:Session=Depends(get_db),
                token:str=Security(security)):
    try:

        user = verify_token(token.credentials)

        if not user["id"]:
            raise HTTPException(status_code=403,detail="yo do not have permission to create this task.")
        # breakpoint()
        task_data = Task_model(title=task.title,description=task.description,status=task.status,owner_id = user["id"])
        db.add(task_data)
        db.commit()
        db.refresh(task_data)
        return{
            "success":True,
            "message":"Task created successfully!",
            "user_id":user["id"]
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
def get_task(owner_id:int,db:Session=Depends(get_db)):
    try:
        data = db.query(Task_model).filter(Task_model.owner_id == owner_id).first()
        if not data:
            raise HTTPException(status_code=404,detail="Task not found")
        return{
            "success":True,
            "message":"This is your task",
            "task_id":data.id
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

def update_task(task:Update_task_schema,db:Session=Depends(get_db)):
    try:
        task1 = db.query(Task_model).filter(Task_model.id == task.id).first()
        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found!"
            )
        task1.title = task.title
        task1.description=task.description
        task1.status = task.status
        task1.owner_id = task.owner_id
        db.commit()
        return {
            "success":True,
            "message":"Task updated successfully!"
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
def delete_task(task_id:int,db:Session=Depends(get_db)):
    try:
        data=db.query(Task_model).filter(Task_model.id == task_id).first()
        if not data:
            raise HTTPException(status_code=404,detail="task not found!!")
        db.delete(data)
        db.commit()
        return{
            "success":True,
            "message":"task deleted successfully!!"
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))