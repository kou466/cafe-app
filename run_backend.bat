@echo off
echo 카페 백엔드 서버를 시작합니다...
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 