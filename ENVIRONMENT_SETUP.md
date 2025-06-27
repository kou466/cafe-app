# 환경 변수 설정 가이드

## 🔧 환경 변수 파일 생성

프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 참고하여 설정하세요:

```bash
# 데이터베이스 설정
DATABASE_URL=sqlite:///./cafe.db
# PostgreSQL 사용시: postgresql://username:password@localhost/database_name

# JWT 설정 (향후 인증 기능 추가시)
SECRET_KEY=your-super-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# FastAPI 설정
DEBUG=True
ENVIRONMENT=development

# CORS 설정
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# 파일 업로드 설정
MAX_FILE_SIZE=5242880  # 5MB in bytes
UPLOAD_DIRECTORY=./uploads

# 로그 설정
LOG_LEVEL=INFO
LOG_FILE=app.log

# Redis 설정 (향후 캐싱 추가시)
REDIS_URL=redis://localhost:6379

# 이메일 설정 (향후 알림 기능 추가시)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# 결제 시스템 설정 (향후 결제 기능 추가시)
PAYMENT_API_KEY=your-payment-api-key
PAYMENT_SECRET_KEY=your-payment-secret-key

# 외부 API 설정
KAKAO_API_KEY=your-kakao-api-key
NAVER_API_KEY=your-naver-api-key
```

## 📝 설정 방법

1. **프로젝트 루트에 `.env` 파일 생성:**
   ```bash
   touch .env  # Linux/Mac
   # 또는 Windows에서 메모장으로 .env 파일 생성
   ```

2. **위 내용을 복사하여 `.env` 파일에 붙여넣기**

3. **실제 값으로 변경:**
   - `your-super-secret-key-here-change-in-production` → 실제 비밀키
   - `your-email@gmail.com` → 실제 이메일
   - 기타 API 키들을 실제 값으로 변경

## 🔒 보안 주의사항

- `.env` 파일은 Git에 커밋하지 마세요 (`.gitignore`에 포함됨)
- 프로덕션 환경에서는 반드시 강력한 SECRET_KEY 사용
- API 키와 비밀번호는 절대 소스코드에 하드코딩하지 마세요

## 🚀 환경별 설정

개발, 테스트, 프로덕션 환경별로 다른 설정을 사용할 수 있습니다:

- `.env.development` - 개발 환경
- `.env.test` - 테스트 환경  
- `.env.production` - 프로덕션 환경

## 📖 FastAPI에서 환경 변수 사용

```python
# backend/app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./cafe.db"
    secret_key: str = "default-secret-key"
    debug: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings() 