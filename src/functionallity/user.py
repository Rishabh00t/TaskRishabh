from fastapi import Depends,HTTPException,Header,status,Security
from database.database import get_db
from sqlalchemy.orm import Session
from src.resource.user.model import User_model
from src.resource.user.schema import User_schema
from src.utils.utils import password_hash
from src.utils.utils import create_access_token,create_refresh_token,verify_token
from fastapi.security import HTTPBearer

security = HTTPBearer()

def create_user(user:User_schema,db:Session=Depends(get_db)):
    try:
        hashed_password = password_hash.hash(user.password)
        userdata = db.query(User_model).filter(User_model.username == user.username).first()
        if userdata:
            raise HTTPException(status_code=404,detail="User name already exist!!")
        
        useremail = db.query(User_model).filter(User_model.email == user.email).first()
        if useremail:
            raise HTTPException(status_code=404,detail="Email already exist!!")
        
        user_db = User_model(username=user.username,password = hashed_password,email = user.email,role = user.role)
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return {
            "Success":True,
            "message":"User created successfully!!",
            "User_id":user_db.id,
            "username":user_db.username

        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
def loginuser(user:User_schema,db:Session=Depends(get_db)):
    try:
        user_db = db.query(User_model).filter(User_model.username==user.username).first()
        if not user_db:
            raise HTTPException(status_code=404,detail="User not found!!")
        if password_hash.verify(user.password,user_db.password):
            access_token = create_access_token(data={"sub":user_db.username,"id":user_db.id})
            refresh_token = create_refresh_token(data={"sub":user_db.username,"id":user_db.id})
            return{
                "success":True,
                "message":"Logging successfully!!",
                "access_token":access_token,
                "refresh_token":refresh_token
            }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

def get_current_user(db:Session = Depends(get_db), auth_token:str=Security(security)):
    try:
        token = (auth_token.credentials)
        token_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"Auth-Token": ""},)
        if not token:
            raise token_exception
        user_id: int = verify_token(token)
        if user_id:
            user = loginuser(db, user_id)
            return user
        raise token_exception
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


def get_all_user_by_admin(db:Session=Depends(get_db),user:User_model = Depends(get_current_user)):
    try:
        # breakpoint()
        if user.role != 'admin':
            raise HTTPException(status_code=403, detail="Operation not permitted")
        users1 = db.query(User_model).all()
        return{"success":True,"users":users1}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
def delete_all_user_by_admin(db:Session=Depends(get_db),user:User_model = Depends(get_current_user)):
    try:
        if user.role != 'admin':
            raise HTTPException(
                status_code=403,
                detail="Operation not permitted"
            )
        user1 = db.query(User_model).all()
        db.delete(user1)
        db.commit()
    except Exception as e:
        raise HTTPException (status_code=500,detail=str(e))