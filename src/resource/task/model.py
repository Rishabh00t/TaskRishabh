from sqlalchemy import *
from database.database import Base
from sqlalchemy.orm import Relationship
from src.resource.user.model import User


class Task(Base):
    __tablename__="tasks"
    id = Column(Integer,primary_key=True)
    title = Column(String(200))
    description = Column(String(300))
    status = Column(String,default="pending")
    owner_id = Column(Integer,ForeignKey('users.id',ondelete='cascade'))
    user = Relationship('User')