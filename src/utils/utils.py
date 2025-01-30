from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime,timedelta
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES,SECRET_KEY,ALGORITHM,REFRESH_TOKEN_EXPIRE_DAY
from fastapi import HTTPException

password_hash =CryptContext(schemes=['bcrypt'],deprecated="auto")
REFRESH_SECRET_KEY="hyy"

def create_access_token(data:dict,expire_delta:timedelta=None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta 
    else: 
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data:dict,expire_delta:timedelta=None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta 
    else: 
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAY)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401,detail=str(e))