"""
Application Configuration Module

환경 변수를 통한 중앙 집중식 설정 관리
개발, 테스트, 프로덕션 환경 분리 지원
"""
from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import validator
import secrets
from pathlib import Path

class Settings(BaseSettings):
    """애플리케이션 설정 클래스"""
    
    # === 기본 설정 ===
    PROJECT_NAME: str = "Cafe Website API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # === 환경 설정 ===
    ENVIRONMENT: str = "development"  # development, test, production
    DEBUG: bool = True
    
    # === 보안 설정 ===
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"
    
    # === 데이터베이스 설정 ===
    # SQLite (기본값)
    DATABASE_URL: Optional[str] = None
    
    # MySQL 설정
    MYSQL_HOST: Optional[str] = None
    MYSQL_PORT: int = 3306
    MYSQL_USER: Optional[str] = None
    MYSQL_PASSWORD: Optional[str] = None
    MYSQL_DATABASE: Optional[str] = None
    
    # 데이터베이스 풀 설정
    DB_POOL_SIZE: int = 5
    DB_POOL_RECYCLE: int = 300  # 5분
    DB_POOL_PRE_PING: bool = True
    
    # === CORS 설정 ===
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
    ]
    
    # === 파일 업로드 설정 ===
    UPLOAD_DIRECTORY: str = "./uploads"
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    
    # === 로깅 설정 ===
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = None
    
    # === 페이지네이션 ===
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    @property
    def database_url(self) -> str:
        """데이터베이스 URL 생성"""
        # MySQL 설정이 있으면 MySQL 사용
        if all([self.MYSQL_HOST, self.MYSQL_USER, self.MYSQL_PASSWORD, self.MYSQL_DATABASE]):
            return (
                f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@"
                f"{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"
            )
        # 환경별 SQLite 데이터베이스
        if self.DATABASE_URL:
            return self.DATABASE_URL
        
        db_file = f"cafe_{self.ENVIRONMENT}.db"
        return f"sqlite:///./db/{db_file}"
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"
    
    @property
    def upload_path(self) -> Path:
        """업로드 디렉토리 Path 객체"""
        path = Path(self.UPLOAD_DIRECTORY)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# 설정 인스턴스 생성
settings = Settings() 