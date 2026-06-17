from sqlalchemy import create_engine, Column, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

Base = declarative_base()

class DatasetRecord(Base):
    __tablename__ = "datasets"
    id           = Column(String, primary_key=True)
    name         = Column(String)
    created_at   = Column(DateTime, default=datetime.datetime.utcnow)
    parquet_path = Column(String)
    schema_json  = Column(Text)

class ProjectRecord(Base):
    __tablename__ = "projects"
    id         = Column(String, primary_key=True)
    name       = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def get_session(db_url: str = "sqlite:///ml_pipeline.db"):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
