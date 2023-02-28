from typing import Optional, Iterable
from datetime import datetime

from sqlalchemy import select, delete, update, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from loguru import logger

from app.database import session_local
from .models import TaskModel
from .schemas import (
    CreateTaskSchema,
    OutTaskSchema,
    UpdateTaskSchrma,
    TasksList
)


class TaskBaseCRUD:
    
    def __enter__(self):
        self._session: Session = session_local()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self._session:
            self._session.close()


class TaskCRUD(TaskBaseCRUD):
    
    def create_task(self, data: CreateTaskSchema) -> Optional[OutTaskSchema]:
        task = TaskModel(
            title=data.title,
            body=data.body,
            is_complited=data.is_complited,
            created_at=data.created_at,
            updated_at=data.updated_at
        )
        result = None
        try:
            self._session.add(task)
            self._session.commit()
            result = OutTaskSchema(
                id=task.id,
                title=task.title,
                body=task.body,
                is_complited=task.is_complited,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
        except IntegrityError as ex:
            logger.warning(ex)
        
        return result
    
    def get_task(self, pk: int) -> OutTaskSchema:
        stmt = select(TaskModel).where(TaskModel.id == pk)
        result: TaskModel = self._session.scalar(stmt)
        return OutTaskSchema(
                id=result.id,
                title=result.title,
                is_complited=result.is_complited,
                created_at=result.created_at,
                updated_at=result.updated_at
            )
    
    def get_task_by_date(self, start_date: datetime, end_date: datetime) -> TasksList:
        stmt = select(TaskModel).where(and_(TaskModel.created_at >= start_date, TaskModel.created_at <= end_date))
        result = self._session.scalars(stmt)
        return self._format_all_tasks(result.fetchall())
    
    def get_all_tasks(self):
        stmt = select(TaskModel)
        result = self._session.scalars(stmt)
        return self._format_all_tasks(result.fetchall())
    
    def update_task(self, pk: int, data: UpdateTaskSchrma) -> None:
        stmt = update(TaskModel).where(TaskModel.id == pk).values(**data.dict())
        self._session.execute(stmt)
        self._session.commit()
    
    def delete_task(self, pk: int) -> None:
        stmt = delete(TaskModel).where(TaskModel.id == pk)
        self._session.execute(stmt)
        self._session.commit()
        
    def _format_all_tasks(self, data: Iterable) -> TasksList:
        return TasksList(tasks=[OutTaskSchema(
                    id=task.id,
                    title=task.title,
                    body=task.body,
                    is_complited=task.is_complited,
                ) for task in data])
        