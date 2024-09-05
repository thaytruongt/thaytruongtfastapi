from typing import Optional
from pydantic import BaseModel, Field
from schemas.base_entity import Gender
from sqlalchemy import Column, ForeignKey, SmallInteger, String, Uuid, Enum
from datetime import datetime
from uuid import UUID
from schemas.company import CompanyMode



class CompanyModel(BaseModel):
    name: str = Field(min_length=2)
    description: Optional[str]
    mode: CompanyMode = Field(default=CompanyMode.DRAFT)
    rating: int = Field(ge=0, le=5, default=0)
    owner_id: Optional[UUID] = None


class CompanyViewModel(BaseModel):
    id: UUID 
    name: str
    description: str
    rating: int
    owner_id: UUID | None = None
  
    
    class Config:
        from_attributes = True
