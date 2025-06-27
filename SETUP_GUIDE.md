# 카페 웹사이트 프로젝트 설정 가이드

## 🏗️ 프로젝트 구조

```
begin_esp/
├── backend/                 # FastAPI 백엔드
│   ├── app/
│   │   ├── api/            # API 엔드포인트
│   │   ├── core/           # 핵심 설정
│   │   ├── db/             # 데이터베이스 설정
│   │   ├── models/         # SQLAlchemy 모델
│   │   └── schemas/        # Pydantic 스키마
│   └── requirements.txt    # Python 패키지 목록
├── frontend/               # 프론트엔드
│   ├── index.html         # 메인 페이지
│   ├── css/               # 스타일시트
│   ├── js/                # JavaScript
│   └── images/            # 이미지 파일
└── run_backend.bat        # 백엔드 실행 스크립트

```

## 🚀 시작하기

### 1. 백엔드 설정

1. **가상환경 생성 및 활성화**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

2. **패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```

3. **데이터베이스 설정**
   - SQLite 사용시: `backend/app/db/base.py`에서 다음과 같이 수정
   ```python
   SQLALCHEMY_DATABASE_URL = "sqlite:///./cafe.db"
   ```
   
   - PostgreSQL 사용시: 데이터베이스를 먼저 생성하고 연결 정보 입력

4. **서버 실행**
   ```bash
   # 프로젝트 루트에서
   run_backend.bat
   
   # 또는 직접 실행
   cd backend
   uvicorn app.main:app --reload
   ```

### 2. 프론트엔드 설정

1. **정적 파일 서버 실행** (Python 사용)
   ```bash
   cd frontend
   python -m http.server 3000
   ```

2. **브라우저에서 확인**
   - http://localhost:3000 접속

## 📋 개발 순서 및 팁

### 추천 개발 순서:
1. **DB 스키마 설계** → 2. **백엔드 API** → 3. **프론트엔드 UI** → 4. **통합 테스트**

### 각 단계별 작업:

#### 1️⃣ 데이터베이스 확장
- 새로운 테이블 추가시:
  1. `backend/app/models/`에 모델 파일 생성
  2. `backend/app/schemas/`에 스키마 파일 생성
  3. Alembic으로 마이그레이션 생성

#### 2️⃣ API 엔드포인트 추가
- `backend/app/api/endpoints/`에 새 라우터 파일 생성
- `backend/app/main.py`에 라우터 등록

#### 3️⃣ 프론트엔드 기능 추가
- React/Vue.js로 전환시:
  ```bash
  npx create-react-app frontend-react
  # 또는
  npm create vue@latest frontend-vue
  ```

## 🔧 추가 기능 구현 아이디어

1. **사용자 인증**
   - JWT 토큰 기반 인증
   - 회원가입/로그인 기능

2. **주문 시스템**
   - 장바구니 기능
   - 주문 내역 관리

3. **관리자 페이지**
   - 메뉴 CRUD
   - 주문 관리

4. **실시간 기능**
   - WebSocket으로 주문 상태 업데이트
   - 실시간 재고 관리

## 🛠️ 문제 해결

### CORS 에러 발생시
`backend/app/main.py`의 CORS 설정 확인:
```python
allow_origins=["http://localhost:3000"]  # 프론트엔드 URL
```

### 데이터베이스 연결 실패시
- PostgreSQL: 서비스 실행 상태 확인
- SQLite: 파일 권한 확인

### API 문서 확인
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc) 