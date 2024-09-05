from sqlalchemy import Boolean, Column, String,ForeignKey, SmallInteger, String, Uuid, Enum
from database import Base
from sqlalchemy.orm import relationship
from schemas.base_entity import BaseEntity
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"])

class User(BaseEntity, Base):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    company_id = Column(Uuid, ForeignKey("companys.id"), nullable=True)

def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hased_password):
    return bcrypt_context.verify(plain_password, hased_password)


user = relationship("Company")


