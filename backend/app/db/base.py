"""
Database Connection Module

SQLAlchemy 엔진, 세션, Base 클래스 설정
환경별 데이터베이스 연결 지원 (SQLite, MySQL)
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 설정에서 데이터베이스 URL 가져오기
engine = create_engine(
    settings.database_url,
    pool_size=settings.DB_POOL_SIZE,
    pool_recycle=settings.DB_POOL_RECYCLE,
    pool_pre_ping=settings.DB_POOL_PRE_PING,
    echo=settings.DEBUG  # 개발 환경에서 SQL 로그 출력
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 데이터베이스 세션 의존성
def get_db():
    """데이터베이스 세션 생성 및 관리"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 