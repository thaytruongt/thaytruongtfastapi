from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from models.user import UserBaseModel # AuthorViewModel



class SearchTaskModel():
    def __init__(self, owner_id,page,size) -> None:
        # self.summary     = summary  
        # self.description = description
        # self.status      = status
        #self.priority    = priority
        self.owner_id     = owner_id
        self.page = page
        self.size = size
        
class TaskModel(BaseModel):
    summary: str
    description: Optional[str]
    status: str
    priority: int = Field(ge=0, le=5, default=0)
    owner_id: UUID| None = None
   
   
    
    class Config:
        json_schema_extra = {
            "example": {
                "summary": "task 1",
                "description": "Description for task 1",
                "status": "status 1",
                "priority": 3,
                "owner_id": "123e4567-e89b-12d3-a456-426614174000",
                
            }
        }

class TaskViewModel(BaseModel):
    id: UUID
    summary: str
    description: str | None = None
    status: str
    priority: int
    owner_id: UUID| None = None
    #user: UserBaseModel
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    class Config:
        from_attributes = True
