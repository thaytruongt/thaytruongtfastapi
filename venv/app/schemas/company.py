import uuid
import enum
from database import Base
from sqlalchemy import Column, ForeignKey, SmallInteger, String, Uuid, Enum
from sqlalchemy.orm import relationship
from .base_entity import BaseEntity


class CompanyMode(enum.Enum):
    DRAFT = 'D'
    PUBLISHED = 'P'

class Company(Base, BaseEntity):
    __tablename__ = "companys"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String)
    mode = Column(Enum(CompanyMode), nullable=False, default=CompanyMode.DRAFT)
    description = Column(String)
    rating = Column(SmallInteger, nullable=False, default=0)
    owner_id= Column(Uuid, ForeignKey("users.id"), nullable=True)
  #
    #users = relationship("User", back_populates="company")
    #owner = relationship("User")
