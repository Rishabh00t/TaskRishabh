from datetime import datetime, timedelta
from fastapi import APIRouter,Depends,HTTPException,Header, Security
from typing import Annotated
from src.resource.user.model import User_model
from src.resource.user.schema import User_schema,Login_schema
from sqlalchemy.orm import Session
from jose import jwt,JWTError
from database.database import get_db
from src.utils.utils import verify_token,create_access_token
from src.functionallity.user import create_user,loginuser,get_all_user_by_admin,get_current_user,delete_all_user_by_admin
from fastapi.security import OAuth2PasswordBearer,HTTPBearer
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES,SECRET_KEY,ALGORITHM,REFRESH_TOKEN_EXPIRE_DAY

# from fastapi_jwt_auth import AuthJWT
user_router = APIRouter()

REFRESH_SECRET_KEY="hyy"

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
        response = loginuser(user=user,db=db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@user_router.get("/protected-route")
def protected_route(token:str=Depends(oauth2_schema)):
    user = verify_token(token)
    return {"success":True,"message":"access granted","user":user}
    
@user_router.get("/get_all_user_by_admin",tags=['admin'])
def get_all_user(db:Session=Depends(get_db),user:User_model = Depends(get_current_user)):
    try:
        response = get_all_user_by_admin(db,user)
        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
@user_router.delete("/delete_all_user",tags=["admin"])
def delete_all_user(user:User_model=Depends(get_current_user),db:Session=Depends(get_db)):
    try:
        response = delete_all_user_by_admin(db,user)
        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
@user_router.get("/get_current_user")
def get_current(db:Session = Depends(get_db), auth_token:str=Security(security)):
    try:
        response = get_current_user(db,auth_token)
        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
# def create_jwt_token(data:dict,expires_delta:timedelta,secret_key:str):
#     expire = datetime.utcnow()+expires_delta
#     data.update({"exp":expire})
#     return jwt.decode(data,secret_key,algorithms=ALGORITHM)

@user_router.post("/get_new_access_token")
def create_access(refresh_token:str=Security(security)):
    try:
        # breakpoint()
        token = refresh_token.credentials

        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        new_access_token = create_access_token(
            data={"sub":payload["sub"]},
            expire_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            secret_key = SECRET_KEY
        )
        return {"access_token":new_access_token}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
# @user_router.post("/refresh")
# async def refresh_token(refresh_token: str = Depends(check_cookie), db: Session = Depends(get_db)):
#     """
#     Create a refresh token route
#     """
#     if not refresh_token:
#         raise HTTPException(status_code=401, detail="No refresh token")
#     decoded_token = await decode_token(refresh_token, 'id', type='refresh')
#     if not decoded_token:
#         raise HTTPException(status_code=401, detail="Invalid refresh token")
#     user = get_user_by_id(db, decoded_token)
#     if not user:
#         raise HTTPException(status_code=401, detail="User does not exist")
#     access_token = create_access_token(data={"sub": user.email})
#     return JSONResponse({"token": access_token, "email": user.email}, status_code=200)
    
# @user_router.post('/refresh')
# def refresh(Authorize: AuthJWT = Depends()):
#     Authorize.jwt_refresh_token_required()
#     current_user = Authorize.get_jwt_subject()
#     new_access_token = Authorize.create_access_token(subject=current_user)
#     return {"access_token": new_access_token}
# @user_router.post("/refresh")  
# async def refresh_access_token(token_data: Annotated[tuple[User_model, str], Depends(verify_token)]):  
#     user, token = token_data  
#     access_token = create_access_token(data={"sub": user.username, "role": user.role}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)  
#     refresh_token = create_refresh_token(data={"sub": user.username, "role": user.role}, expires_delta=REFRESH_TOKEN_EXPIRE_DAY)  
  
#     refresh_tokens.remove(token)  
#     refresh_tokens.append(refresh_token)  
#     return(access_token=access_token, refresh_token=refresh_token)