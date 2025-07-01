from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logger import logger
from app.db.base import engine, Base
from app.api.endpoints import menu
from app.models import Category, Menu, User, Order, OrderItem  # 모든 모델 import

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # 시작 시 실행
    logger.info("=== 카페 API 서버 시작 ===")
    logger.info(f"환경: {settings.ENVIRONMENT}")
    logger.info(f"데이터베이스: {settings.database_url.split('://')[0]}")
    
    # 데이터베이스 테이블 생성
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("데이터베이스 테이블 생성 완료")
    except Exception as e:
        logger.error(f"데이터베이스 테이블 생성 실패: {e}")
        raise
    
    yield
    
    # 종료 시 실행
    logger.info("=== 카페 API 서버 종료 ===")

# FastAPI 앱 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="카페 웹사이트를 위한 REST API - 메뉴 관리, 주문 시스템, 사용자 인증 제공",
    version=settings.VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(
    menu.router, 
    prefix=settings.API_V1_STR, 
    tags=["메뉴"]
)

# 루트 엔드포인트
@app.get("/")
async def read_root():
    """API 루트 엔드포인트"""
    return {
        "message": f"{settings.PROJECT_NAME}에 오신 것을 환영합니다!",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "health_check": "/health"
    }

@app.get("/health")
async def health_check():
    """서버 상태 확인"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

@app.get("/info")
async def app_info():
    """애플리케이션 정보"""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "cors_origins": settings.BACKEND_CORS_ORIGINS
    } 