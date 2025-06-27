from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL 사용 예시 (SQLite로 변경 가능)
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/cafe_db"
# SQLite 사용시: "sqlite:///./cafe.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 