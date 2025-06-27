from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import menu
from app.db.base import engine, Base

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
app = FastAPI(
    title="카페 API",
    description="카페 웹사이트를 위한 REST API",
    version="1.0.0"
)

# CORS 설정 (프론트엔드와 통신을 위해)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포시에는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(menu.router, prefix="/api/v1", tags=["menu"])

@app.get("/")
def read_root():
    return {"message": "카페 API에 오신 것을 환영합니다!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"} 