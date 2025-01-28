from sqlalchemy import *
from database.database import Base


class User_model(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    username = Column(String(200))
    email = Column(String(200))
    password = Column(String(200))
    role = Column(String(200))