from pydantic import BaseModel


class Tasks_schema(BaseModel):
    title:str
    description:str
    status:str

class Update_task_schema(BaseModel):
    id:int
    title:str
    description:str
    status:str
    owner_id:int