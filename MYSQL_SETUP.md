# MySQL 연동 설정 가이드

## 🔧 OCI A1 인스턴스 MySQL 연동

### 1. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 입력:

```bash
# MySQL 연동 설정 (OCI A1 인스턴스)
MYSQL_HOST=your-oci-instance-ip
MYSQL_PORT=3306
MYSQL_USER=your-mysql-username
MYSQL_PASSWORD=your-mysql-password
MYSQL_DATABASE=cafe_db

# FastAPI 설정
SECRET_KEY=your-super-secret-key-here
DEBUG=True
ENVIRONMENT=development

# CORS 설정
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 2. MySQL 데이터베이스 준비

OCI 인스턴스에서 MySQL 데이터베이스 생성:

```sql
-- MySQL에 접속 후 실행
CREATE DATABASE cafe_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 사용자 생성 및 권한 부여 (필요시)
CREATE USER 'cafe_user'@'%' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON cafe_db.* TO 'cafe_user'@'%';
FLUSH PRIVILEGES;
```

### 3. 방화벽 설정 확인

OCI 인스턴스에서 3306 포트가 열려있는지 확인:

```bash
# Ubuntu/CentOS에서
sudo ufw allow 3306
# 또는
sudo firewall-cmd --permanent --add-port=3306/tcp
sudo firewall-cmd --reload
```

### 4. MySQL 외부 접속 허용

MySQL 설정 파일 수정:

```bash
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf

# bind-address 주석 처리 또는 변경
# bind-address = 127.0.0.1  # 이 줄을 주석 처리
bind-address = 0.0.0.0      # 또는 이렇게 변경

# MySQL 재시작
sudo systemctl restart mysql
```

### 5. 패키지 설치 및 테스트

```bash
# 새로운 패키지 설치
pip install -r requirements.txt

# 데이터베이스 연결 테스트
python -c "
from backend.app.core.config import settings
print('Database URL:', settings.database_url)
"

# 테이블 생성 및 데이터 추가
python backend/init_test_data.py
```

### 6. 트러블슈팅

**연결 실패 시 체크리스트:**

1. OCI 보안 목록에서 3306 포트 열림 확인
2. MySQL 사용자 권한 확인
3. 방화벽 설정 확인
4. MySQL 서비스 상태 확인: `sudo systemctl status mysql`
5. 네트워크 연결 테스트: `telnet your-oci-ip 3306`

**일반적인 오류 해결:**

```bash
# "Authentication plugin 'caching_sha2_password' cannot be loaded" 오류 시
ALTER USER 'your-user'@'%' IDENTIFIED WITH mysql_native_password BY 'your-password';
FLUSH PRIVILEGES;
```

### 7. 개발/운영 환경 분리

**.env.development**
```bash
MYSQL_HOST=localhost
MYSQL_DATABASE=cafe_dev
```

**.env.production**
```bash
MYSQL_HOST=your-oci-instance-ip
MYSQL_DATABASE=cafe_prod
``` 