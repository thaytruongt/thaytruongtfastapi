from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
    company_id: UUID | None = None

class UserBaseModel(BaseModel):
    id: UUID
    username: str
    email: str | None = None
    first_name: str
    last_name: str
    is_admin: bool
    company_id: UUID| None = None
    
    class Config:
        from_attributes = True

class UserViewModel(UserBaseModel):
    is_admin: bool
    is_active: bool
    company_id: UUID| None = None
    created_at: datetime | None = None
    update_at: datetime | None = None
