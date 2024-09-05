
# import uuid
# import enum
from database import Base
from sqlalchemy import Column, ForeignKey, SmallInteger, String, Uuid, Enum
from sqlalchemy.orm import relationship
from .base_entity import BaseEntity
#from schemas.user import User


class Task(BaseEntity, Base):
    __tablename__ = "tasks"

    summary = Column(String)
    description = Column(String)
    status = Column(String)
    priority = Column(SmallInteger, nullable=False, default=0)
    owner_id = Column(Uuid, ForeignKey("users.id"), nullable=True)
    
    

   
    owner = relationship("User")
