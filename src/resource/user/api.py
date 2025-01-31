from datetime import datetime, timedelta
from fastapi import APIRouter,Depends,HTTPException,Header, Security
from typing import Annotated
from src.resource.user.model import User
from src.resource.user.schema import User_schema,Login_schema
from sqlalchemy.orm import Session
from jose import jwt,JWTError
from database.database import get_db
from src.utils.utils import verify_token,create_access_token
from src.functionallity.user import create_user,login_user,get_all_user_by_admin,delete_all_user_by_admin
from fastapi.security import OAuth2PasswordBearer,HTTPBearer,HTTPAuthorizationCredentials
from src.config import Config

ACCESS_TOKEN_EXPIRE_MINUTES= Config.ACCESS_TOKEN_EXPIRE
SECRET_KEY = Config.SEC_KEY
ALGORITHM = Config.ALGO
REFRESH_TOKEN_EXPIRE_DAY = Config.REFRESH_TOKEN_EXPIRE

user_router = APIRouter()

security = HTTPBearer()
oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

@user_router.post("/register",tags=['Register & generate tokens'])
def user_signup(user:User_schema,db:Session=Depends(get_db)):
    try:
        response = create_user(user,db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@user_router.post("/login",tags=['Register & generate tokens'])
def user_login_details(user:Login_schema,db:Session=Depends(get_db)):
    try:
        response = login_user(user=user,db=db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@user_router.get("/protected-route")
def protected_route(token:str=Depends(oauth2_schema)):
    user = verify_token(token)
    return {"success":True,"message":"access granted","user":user}
    
@user_router.get("/get_all_user_by_admin",tags=['admin'])
def get_all_user(user_id:int,db:Session=Depends(get_db)):
    try:
        response = get_all_user_by_admin(db=db,user_id=user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@user_router.delete("/delete_all_user",tags=["admin"])
def delete_all_user(user_id:int,db:Session=Depends(get_db)):
    try:
        response = delete_all_user_by_admin(db=db,user_id=user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
   

@user_router.post("/get_new_access_token")
def create_access(refresh_token:HTTPAuthorizationCredentials=Security(security)):
    try:
        # breakpoint()
        token = refresh_token.credentials

        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        new_access_token = create_access_token(
            data={"sub":payload["sub"]},
            expire_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token":new_access_token}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))