from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from services import utils
from models.user import UserModel
from services import company as CompanyService
from schemas.user import User
from services.exception import ResourceNotFoundError,InvalidInputError


async def get_users(async_db: AsyncSession) -> list[User]:
    result = await async_db.scalars(select(User).order_by(User.username))
    
    return result.all()

def get_user_by_id(db: Session, user_id: UUID) -> User:
    return db.scalars(select(User).filter(User.id == user_id)).first()

def add_new_user(db: Session, data: UserModel) -> User:
    company = CompanyService.get_company_by_id(db, data.company_id)
        
    if company is None:
        raise InvalidInputError("Invalid company information")
    
    user = User(**data.model_dump())
    user.created_at = utils.get_current_utc_time()
    user.updated_at = utils.get_current_utc_time()
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


def update_user(db: Session, id: UUID, data: UserModel) -> User:
    user = get_user_by_id(db, id)

    if user is None:
        raise ResourceNotFoundError()

    if data.company_id != user.company_id:
        company = CompanyService.get_company_by_id(db, data.company_id)
        if company is None:
            raise InvalidInputError("Invalid company information")
    
    user.username = data.username
    user.email = data.email
    user.first_name = data.first_name
    user.last_name = data.last_name
    user.password = data.password
    user.company_id =data.company_id
    user.updated_at = utils.get_current_utc_time()
    
    
    db.commit()
    db.refresh(user)
    return user