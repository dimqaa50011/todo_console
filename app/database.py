from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from .config import SQLALCHEMY_DATABASE_URI


engine = create_engine(SQLALCHEMY_DATABASE_URI)
session_local = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)
Base = declarative_base()
