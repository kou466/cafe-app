# 개발 환경 동기화 가이드

## 🔄 랩탑 ↔ PC 개발 환경 이동

### **🏆 추천 방법: Git + 클라우드 DB**

#### **1. Git 리포지토리 설정**

```bash
# 랩탑에서 (현재 환경)
git add .
git commit -m "카페 프로젝트 기본 구조 완성"

# GitHub/GitLab 리포지토리 생성 후
git remote add origin https://github.com/yourusername/cafe-project.git
git push -u origin master
```

#### **2. PC에서 프로젝트 복제**

```bash
# PC에서
git clone https://github.com/yourusername/cafe-project.git
cd cafe-project

# Conda 환경 생성
conda create -n begin python=3.12 -y
conda activate begin

# 패키지 설치
cd backend
pip install -r requirements.txt
```

#### **3. 환경 변수 동기화**

PC에서 `.env` 파일 생성 (MySQL 연동):
```bash
# PC의 .env 파일
MYSQL_HOST=your-oci-instance-ip
MYSQL_PORT=3306
MYSQL_USER=your-mysql-username
MYSQL_PASSWORD=your-mysql-password
MYSQL_DATABASE=cafe_db

SECRET_KEY=your-super-secret-key-here
DEBUG=True
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### **🔧 다른 방법들**

#### **방법 2: 클라우드 IDE (GitHub Codespaces)**

```bash
# GitHub 리포지토리에서 Codespaces 시작
# 자동으로 동기화됨, 어디서든 접근 가능
```

#### **방법 3: Docker 컨테이너화**

```dockerfile
# Dockerfile 생성으로 환경 통일
FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0"]
```

#### **방법 4: 클라우드 드라이브 + 환경 스크립트**

```bash
# 프로젝트를 OneDrive/Google Drive에 저장
# setup.sh 스크립트로 환경 자동 설정
```

### **📋 동기화 체크리스트**

#### **랩탑에서 작업 완료 시:**
- [ ] `git add .`
- [ ] `git commit -m "작업 내용"`
- [ ] `git push origin master`
- [ ] 데이터베이스 변경사항이 있다면 OCI MySQL에 반영

#### **PC에서 작업 시작 시:**
- [ ] `git pull origin master`
- [ ] `conda activate begin`
- [ ] 새로운 패키지가 있다면 `pip install -r requirements.txt`
- [ ] 환경 변수 확인 (`.env` 파일)
- [ ] 서버 실행 테스트

### **🚨 주의사항**

1. **민감 정보 관리:**
   - `.env` 파일은 Git에 포함하지 말 것
   - 각 환경에서 수동으로 생성

2. **데이터베이스 동기화:**
   - 개발용과 테스트용 데이터베이스 분리 추천
   - 스키마 변경 시 마이그레이션 스크립트 사용

3. **Node.js/프론트엔드 동기화:**
   ```bash
   # 프론트엔드 의존성이 있을 경우
   npm install  # package.json 기반으로 동기화
   ```

### **🔄 실시간 동기화 도구 (고급)**

#### **VS Code Live Share**
- 실시간 코드 공유 및 협업
- 같은 프로젝트를 여러 기기에서 동시 편집

#### **Git Hooks**
```bash
# .git/hooks/post-commit
#!/bin/bash
# 커밋 후 자동으로 원격 리포지토리에 푸시
git push origin master
```

### **⚡ 빠른 전환 스크립트**

#### **랩탑용 (push_work.sh)**
```bash
#!/bin/bash
git add .
git commit -m "작업 저장: $(date)"
git push origin master
echo "작업이 저장되었습니다. PC에서 계속 작업 가능합니다."
```

#### **PC용 (pull_work.sh)**
```bash
#!/bin/bash
git pull origin master
conda activate begin
echo "최신 코드가 동기화되었습니다. 작업을 시작하세요."
```

### **🎯 권장 워크플로우**

1. **Git 기반 동기화** (기본)
2. **MySQL 클라우드 DB 공유** (데이터 일관성)
3. **환경 변수 문서화** (빠른 설정)
4. **자동화 스크립트** (편의성)

이 방법으로 랩탑과 PC 간 완벽한 동기화가 가능합니다! 🚀 