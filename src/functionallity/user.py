from fastapi import Depends,HTTPException
from database.database import get_db
from sqlalchemy.orm import Session
from src.resource.user.model import User
from src.resource.user.schema import User_schema
from src.utils.utils import password_hash
from src.utils.utils import create_access_token,create_refresh_token,verify_token
from fastapi.security import HTTPBearer

security = HTTPBearer()

def create_user(user:User_schema,db:Session=Depends(get_db)):
        hashed_password = password_hash.hash(user.password)
        userdata = db.query(User).filter(User.username == user.username).first()
        if userdata:
            raise HTTPException(status_code=404,detail="User name already exist!!")
        
        useremail = db.query(User).filter(User.email == user.email).first()
        if useremail:
            raise HTTPException(status_code=404,detail="Email already exist!!")
        
        user_db = User(username=user.username,password = hashed_password,email = user.email,role = user.role)
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return {
            "success":True,
            "message":"User created successfully!!",
            "user_id":user_db.id,
            "username":user_db.username

        }
    
def login_user(user:User_schema,db:Session=Depends(get_db)):
        user_db = db.query(User).filter(User.username==user.username).first()
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

def get_all_user_by_admin(user_id:int,db:Session=Depends(get_db)):
        user = db.query(User).filter(User.id == user_id).first()
        
        # breakpoint()
        if user.role != 'admin':
            return HTTPException(status_code=403, detail="Operation not permitted")
        users1 = db.query(User).all()
        return{"success":True,"users":users1}
    
def delete_all_user_by_admin(user_id: int, db: Session = Depends(get_db)):
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return HTTPException(status_code=404, detail="User not found")
        
        if user.role != 'admin':
            return HTTPException(status_code=403, detail="Operation not permitted")
        
        deleted_users = db.query(User).filter(User.role != 'admin').delete()
        
        db.commit()

        if deleted_users:
            return {"success": True, "message": "All non-admin users deleted"}
        else:
            return {"success": False, "message": "No users to delete"}
