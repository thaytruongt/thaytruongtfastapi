from typing import List
# from uuid import UUID
# from sqlalchemy import select
# from sqlalchemy.orm import Session, joinedload
# from schemas.task import Task
# from schemas.user import User
# from models.task import TaskModel, SearchTaskModel
# from services import user as UserService
# from services.utils import get_current_utc_time
# from services.exception import ResourceNotFoundError, InvalidInputError



from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session,joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from services import utils
from models.task import TaskModel,SearchTaskModel
from schemas.task import Task
from services.exception import ResourceNotFoundError,InvalidInputError
from services import user as UserService
from services import company as CompanyService
from schemas.user import User
from schemas.company import Company
from services.utils import get_current_utc_time


# def get_tasks(db: Session, conds: SearchTaskModel) -> List[Task]:
#     # Default of joinedload is LEFT OUTER JOIN
#     query = select(Task).options(
#         joinedload(Task.owner))
    
    
#     if conds.summary is not None:
#         query = query.filter(Task.summary.like(f"{conds.summary}%"))
#     if conds.owner_id is not None:
#         query = query.filter(Task.owner_id == conds.owner_id)
   
#     query.offset((conds.page-1)*conds.size).limit(conds.size)
    
#     return db.scalars(query).all()

async def get_tasks(async_db: AsyncSession) -> list[Task]:
    result = await async_db.scalars(select(Task).order_by(Task.created_at))
    
    return result.all()

def get_task_by_id(db: Session, task_id: UUID) -> Task:
    #query = select(Task).filter(Task.id == id)
    return db.scalars(select(Task).filter(Task.id ==task_id)).first()
    
def get_task_by_owner_id(db: Session, conds: SearchTaskModel, async_db: AsyncSession) -> Task:
   ## query = select(Task).filter(Task.owner_id == conds.owner_id)   
    owner = UserService.get_user_by_id(db, conds.owner_id)
    if owner is not None:
        company = CompanyService.get_company_by_id(db,owner.company_id)
        #if user is ad_min and owner of company and then return all tasks
        if owner.is_admin ==True and company is not None and company.owner_id== owner.id:
         query =select(Task)
         #return only task of user
        else:
           #query.options(joinedload(Task.owner, innerjoin=True)).filter(Task.owner_id ==  conds.owner_id)
           query = select(Task).filter(Task.owner_id == conds.owner_id) 
    else:      
       raise InvalidInputError("Invalid owner information")
    
    query.offset((conds.page-1)*conds.size).limit(conds.size)
    return db.scalars(query).all()
    
    
def add_new_task(db: Session, data: TaskModel) -> Task:
    owner = UserService.get_user_by_id(db, data.owner_id)
        
    if owner is None:
        raise InvalidInputError("Invalid owner information")

    task = Task(**data.model_dump())
    task.created_at = get_current_utc_time()
    task.updated_at = get_current_utc_time()

    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task

def update_task(db: Session, id: UUID, data: TaskModel) -> Task:
    task = get_task_by_id(db, id)

    if task is None:
        raise ResourceNotFoundError()

    if data.owner_id != task.owner_id:
        owner = UserService.get_user_by_id(db, data.owner_id)
        if owner is None:
            raise InvalidInputError("Invalid owner information")
    
    task.summary = data.summary
    task.description = data.description
    task.status = data.status
    task.priority= data.priority
    task.owner_id=data.owner_id
    task.updated_at = get_current_utc_time()
    
    db.commit()
    db.refresh(task)
    return task
