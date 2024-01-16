from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.base import Base
from configs.config import db_string

engine = create_engine(db_string, echo=False)
Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)


