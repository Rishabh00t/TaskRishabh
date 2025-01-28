from sqlalchemy import *
from database.database import Base
from sqlalchemy.orm import Relationship
from src.resource.user.model import User_model


class Task_model(Base):
    __tablename__="tasks"
    id = Column(Integer,primary_key=True)
    title = Column(String(200))
    description = Column(String(300))
    status = Column(String(200))
    owner_id = Column(Integer,ForeignKey('users.id',ondelete='cascade'))
    user = Relationship('User_model')