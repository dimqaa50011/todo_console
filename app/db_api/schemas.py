from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str = Field(...)
    body: str = Field(default=None)


class UpdateTaskSchrma(TaskBase):
    is_complited: bool = Field(default=False)
    updated_at: datetime = Field(default=datetime.now())


class CreateTaskSchema(UpdateTaskSchrma):
    created_at: datetime = Field(default=datetime.now())


class OutTaskSchema(CreateTaskSchema):
    id: int = Field(...)


class TasksList(BaseModel):
    tasks: List[OutTaskSchema]
    