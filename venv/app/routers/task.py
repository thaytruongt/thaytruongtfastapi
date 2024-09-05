from typing import List
from uuid import UUID
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db_context,get_db_context
from services import task as TaskService
from services import auth as AuthService
from services.exception import *
from schemas.user import User
from models.task import TaskModel, TaskViewModel, SearchTaskModel

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("", response_model=list[TaskViewModel])
async def get_all_tasks(async_db: AsyncSession = Depends(get_async_db_context)):
    return await TaskService.get_tasks(async_db)

# This is a mock data for testing
# BOOKS = [{"id": i, "name": f"Book {i}", "author": f"Author {i%3 + 1}"} for i in range(1, 11)]


# @router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskViewModel)
# async def get_task_by_id(task_id: UUID, db: Session = Depends(get_db_context)):    
#     task = TaskService.get_task_by_id(db, task_id)

#     if task is None:
#         raise ResourceNotFoundError()

#     return task



@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskViewModel)
async def create_task(
    request: TaskModel,   
   user: User = Depends(AuthService.token_interceptor),
    db: Session = Depends(get_db_context),
    ):
        if not user:
            raise AccessDeniedError() 
        
        request.owner_id = user.id

        return TaskService.add_new_task(db, request)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[TaskViewModel])
async def get_tasks_by_owner(
    owner_id: UUID = Query(default=None),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    db: Session = Depends(get_db_context),
    async_db: AsyncSession = Depends(get_async_db_context),
   # user: User = Depends(AuthService.token_interceptor),
    ):
        # if not user.is_admin:
        #     raise AccessDeniedError()

        conds = SearchTaskModel( owner_id, page, size)
        return TaskService.get_task_by_owner_id(db, conds,async_db)
    
    
    

# @router.get("/{task_id}",status_code=status.HTTP_200_OK, response_model=TaskViewModel)
# async def get_task_detail(task_id: UUID, db: Session=Depends(get_db_context)):
#     task = TaskService.get_task_by_id(db, task_id)
    
#     print('task id')
#     if task is None:
#         raise ResourceNotFoundError()

#     return task


@router.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskViewModel)
async def update_task(
    task_id: UUID,
    request: TaskModel,
    db: Session=Depends(get_db_context),
    ):
        return TaskService.update_task(db, task_id, request)
