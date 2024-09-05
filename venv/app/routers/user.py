from typing import List
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session
from uuid import UUID

from database import get_db_context
from schemas.user import User
from models.user import UserViewModel, UserBaseModel,UserModel
from services import user as UserService


router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", status_code=status.HTTP_200_OK, response_model=List[UserBaseModel])
async def get_users(db: Session = Depends(get_db_context)) -> List[UserViewModel]:
    return db.query(User).filter(User.is_active == True).all()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserViewModel)
async def create_user(request: UserModel, db: Session = Depends(get_db_context)):
    return UserService.add_new_user(db, request)


@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserViewModel)
async def update_user(
    user_id: UUID,
    request: UserModel,
    db: Session = Depends(get_db_context),
    ):
        return UserService.update_user(db, user_id, request)

