from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 설정에서 데이터베이스 URL 가져오기
SQLALCHEMY_DATABASE_URL = settings.database_url

# MySQL과 SQLite 모두 지원하는 엔진 생성
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    # SQLite용 설정
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # MySQL용 설정
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=settings.DB_POOL_PRE_PING,  # 연결 상태 확인
        pool_recycle=settings.DB_POOL_RECYCLE,    # 연결 재사용 시간
        pool_size=settings.DB_POOL_SIZE,          # 연결 풀 크기
        echo=settings.DEBUG   # 개발 환경에서 SQL 로그 출력
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 데이터베이스 세션 의존성
def get_db():
    """데이터베이스 세션 의존성"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 