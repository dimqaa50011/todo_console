from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.database import Base


class TaskModel(Base):
    __tablename__ = 'task'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False, unique=True)
    body = Column(String)
    is_complited = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    def __str__(self) -> str:
        return f'pk: {self.id} | title: {self.title}'
