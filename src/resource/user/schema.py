from pydantic import BaseModel,EmailStr

class User_schema(BaseModel):
    username:str
    password:str
    email:EmailStr
    role:str

class Login_schema(BaseModel):
    username:str
    password:str