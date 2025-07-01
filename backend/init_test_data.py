"""
테스트 데이터 초기화 스크립트

새로운 설정 시스템과 확장된 모델을 사용하여 테스트 데이터를 생성합니다.
"""
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from app.core.config import settings
    from app.core.logger import logger
    from app.db.base import engine, Base, SessionLocal
    from app.models import Category, Menu, User, Order, OrderItem, OrderStatus
    from passlib.context import CryptContext
except ImportError as e:
    print(f"❌ Import 에러: {e}")
    print("현재 작업 디렉토리:", os.getcwd())
    print("Python 경로:", sys.path)
    raise

# 비밀번호 해싱 컨텍스트
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """비밀번호 해싱"""
    return pwd_context.hash(password)

def init_database():
    """데이터베이스 초기화"""
    try:
        logger.info("=== 테스트 데이터 초기화 시작 ===")
        logger.info(f"환경: {settings.ENVIRONMENT}")
        logger.info(f"데이터베이스: {settings.database_url}")
        
        # 테이블 생성
        Base.metadata.create_all(bind=engine)
        logger.info("데이터베이스 테이블 생성 완료")
        
        return True
    except Exception as e:
        logger.error(f"데이터베이스 초기화 실패: {e}")
        return False

def clear_existing_data(db):
    """기존 데이터 삭제"""
    try:
        # 순서 중요: 외래키 관계 고려
        db.query(OrderItem).delete()
        db.query(Order).delete()
        db.query(Menu).delete()
        db.query(Category).delete()
        db.query(User).delete()
        db.commit()
        logger.info("기존 데이터 삭제 완료")
    except Exception as e:
        logger.error(f"기존 데이터 삭제 실패: {e}")
        db.rollback()
        raise

def create_categories(db):
    """카테고리 데이터 생성"""
    categories_data = [
        {"name": "커피", "display_order": 1},
        {"name": "논커피", "display_order": 2},
        {"name": "디저트", "display_order": 3},
        {"name": "베이커리", "display_order": 4},
        {"name": "시즌메뉴", "display_order": 5},
    ]
    
    categories = {}
    for cat_data in categories_data:
        category = Category(**cat_data)
        db.add(category)
        db.commit()
        db.refresh(category)
        categories[cat_data["name"]] = category
        logger.info(f"카테고리 생성: {category.name} (ID: {category.id})")
    
    return categories

def create_menus(db, categories):
    """메뉴 데이터 생성 (이미지 URL 제거됨)"""
    menus_data = [
        # 커피
        {
            "name": "아메리카노",
            "category_id": categories["커피"].id,
            "price": 4500,
            "description": "진한 에스프레소와 뜨거운 물의 조화",
            "is_available": True
        },
        {
            "name": "카페라떼",
            "category_id": categories["커피"].id,
            "price": 5000,
            "description": "부드러운 우유와 에스프레소의 완벽한 밸런스",
            "is_available": True
        },
        {
            "name": "카푸치노",
            "category_id": categories["커피"].id,
            "price": 5000,
            "description": "풍성한 우유 거품과 에스프레소",
            "is_available": True
        },
        {
            "name": "바닐라 라떼",
            "category_id": categories["커피"].id,
            "price": 5500,
            "description": "달콤한 바닐라 시럽이 들어간 카페라떼",
            "is_available": True
        },
        {
            "name": "카라멜 마키아토",
            "category_id": categories["커피"].id,
            "price": 6000,
            "description": "달콤한 카라멜과 에스프레소의 만남",
            "is_available": True
        },
        
        # 논커피
        {
            "name": "녹차라떼",
            "category_id": categories["논커피"].id,
            "price": 5500,
            "description": "고급 녹차 파우더로 만든 건강한 라떼",
            "is_available": True
        },
        {
            "name": "초코라떼",
            "category_id": categories["논커피"].id,
            "price": 5500,
            "description": "진한 초콜릿과 우유의 달콤한 만남",
            "is_available": True
        },
        {
            "name": "레모네이드",
            "category_id": categories["논커피"].id,
            "price": 6000,
            "description": "상큼한 레몬으로 만든 시원한 음료",
            "is_available": True
        },
        {
            "name": "딸기라떼",
            "category_id": categories["논커피"].id,
            "price": 6500,
            "description": "달콤한 딸기와 우유의 조합",
            "is_available": True
        },
        
        # 디저트
        {
            "name": "티라미수",
            "category_id": categories["디저트"].id,
            "price": 6500,
            "description": "이탈리아 정통 디저트",
            "is_available": True
        },
        {
            "name": "치즈케이크",
            "category_id": categories["디저트"].id,
            "price": 6000,
            "description": "부드럽고 진한 뉴욕 스타일 치즈케이크",
            "is_available": False  # 품절 예시
        },
        {
            "name": "브라우니",
            "category_id": categories["디저트"].id,
            "price": 5500,
            "description": "진한 초콜릿이 가득한 촉촉한 브라우니",
            "is_available": True
        },
        
        # 베이커리
        {
            "name": "크로와상",
            "category_id": categories["베이커리"].id,
            "price": 3500,
            "description": "버터 향이 가득한 프랑스 정통 크로와상",
            "is_available": True
        },
        {
            "name": "베이글",
            "category_id": categories["베이커리"].id,
            "price": 3000,
            "description": "쫄깃한 플레인 베이글",
            "is_available": True
        },
        {
            "name": "스콘",
            "category_id": categories["베이커리"].id,
            "price": 4000,
            "description": "영국식 전통 스콘",
            "is_available": True
        },
        
        # 시즌메뉴
        {
            "name": "아이스 아메리카노",
            "category_id": categories["시즌메뉴"].id,
            "price": 4000,
            "description": "시원한 아이스 아메리카노",
            "is_available": True
        },
        {
            "name": "프라페",
            "category_id": categories["시즌메뉴"].id,
            "price": 7000,
            "description": "여름 한정 시원한 프라페",
            "is_available": True
        },
    ]
    
    menus = []
    for menu_data in menus_data:
        menu = Menu(**menu_data)
        db.add(menu)
        menus.append(menu)
    
    db.commit()
    
    # 메뉴 새로고침
    for menu in menus:
        db.refresh(menu)
        logger.info(f"메뉴 생성: {menu.name} (ID: {menu.id}, 가격: {menu.price}원)")
    
    return menus

def create_users(db):
    """사용자 데이터 생성"""
    users_data = [
        {
            "username": "admin",
            "email": "admin@cafe.com",
            "hashed_password": hash_password("admin123"),
            "is_admin": True,
            "is_active": True
        },
        {
            "username": "user1",
            "email": "user1@example.com",
            "hashed_password": hash_password("user123"),
            "is_admin": False,
            "is_active": True
        },
        {
            "username": "user2",
            "email": "user2@example.com",
            "hashed_password": hash_password("user123"),
            "is_admin": False,
            "is_active": True
        },
    ]
    
    users = []
    for user_data in users_data:
        user = User(**user_data)
        db.add(user)
        users.append(user)
    
    db.commit()
    
    # 사용자 새로고침
    for user in users:
        db.refresh(user)
        role = "관리자" if user.is_admin else "일반사용자"
        logger.info(f"사용자 생성: {user.username} ({role}, ID: {user.id})")
    
    return users

def create_sample_orders(db, users, menus):
    """샘플 주문 데이터 생성"""
    # 샘플 주문 생성
    orders_data = [
        {
            "user_id": users[1].id,  # user1
            "customer_name": "김철수",
            "customer_phone": "010-1234-5678",
            "status": OrderStatus.COMPLETED,
            "pickup_time": datetime.now() - timedelta(hours=2),
            "notes": "얼음 많이 넣어주세요"
        },
        {
            "user_id": users[2].id,  # user2
            "customer_name": "이영희",
            "customer_phone": "010-9876-5432",
            "status": OrderStatus.PREPARING,
            "pickup_time": datetime.now() + timedelta(minutes=30),
            "notes": "테이크아웃입니다"
        },
        {
            "user_id": None,  # 비회원 주문
            "customer_name": "박민수",
            "customer_phone": "010-5555-6666",
            "status": OrderStatus.PENDING,
            "pickup_time": datetime.now() + timedelta(hours=1),
            "notes": ""
        }
    ]
    
    orders = []
    for i, order_data in enumerate(orders_data):
        order = Order(**order_data)
        db.add(order)
        db.commit()
        db.refresh(order)
        
        # 주문 아이템 추가
        if i == 0:  # 첫 번째 주문: 아메리카노 2개, 치즈케이크 1개
            items = [
                {"menu_id": menus[0].id, "quantity": 2, "options": "얼음 많이"},
                {"menu_id": menus[10].id, "quantity": 1, "options": ""}
            ]
        elif i == 1:  # 두 번째 주문: 카페라떼 1개, 크로와상 1개
            items = [
                {"menu_id": menus[1].id, "quantity": 1, "options": "디카페인"},
                {"menu_id": menus[13].id, "quantity": 1, "options": "따뜻하게"}
            ]
        else:  # 세 번째 주문: 바닐라라떼 1개
            items = [
                {"menu_id": menus[3].id, "quantity": 1, "options": "시럽 적게"}
            ]
        
        total_amount = 0
        for item_data in items:
            menu = next(m for m in menus if m.id == item_data["menu_id"])
            subtotal = menu.price * item_data["quantity"]
            total_amount += subtotal
            
            order_item = OrderItem(
                order_id=order.id,
                menu_id=item_data["menu_id"],
                quantity=item_data["quantity"],
                price=menu.price,
                subtotal=subtotal,
                options=item_data["options"]
            )
            db.add(order_item)
        
        # 주문 총액 업데이트
        order.total_amount = total_amount
        db.commit()
        db.refresh(order)
        
        orders.append(order)
        logger.info(f"주문 생성: {order.customer_name} (ID: {order.id}, 총액: {order.total_amount}원)")
    
    return orders

def main():
    """메인 실행 함수"""
    try:
        # 데이터베이스 초기화
        if not init_database():
            return False
        
        # 세션 생성
        db = SessionLocal()
        
        try:
            # 기존 데이터 삭제
            clear_existing_data(db)
            
            # 카테고리 생성
            categories = create_categories(db)
            
            # 메뉴 생성
            menus = create_menus(db, categories)
            
            # 사용자 생성
            users = create_users(db)
            
            # 샘플 주문 생성
            orders = create_sample_orders(db, users, menus)
            
            logger.info("=== 테스트 데이터 생성 완료 ===")
            logger.info(f"✅ 카테고리: {len(categories)}개")
            logger.info(f"✅ 메뉴: {len(menus)}개")
            logger.info(f"✅ 사용자: {len(users)}개")
            logger.info(f"✅ 주문: {len(orders)}개")
            
            print("\n=== 🎉 테스트 데이터가 성공적으로 생성되었습니다! ===")
            print(f"카테고리: {len(categories)}개")
            print(f"메뉴: {len(menus)}개")
            print(f"사용자: {len(users)}개")
            print(f"주문: {len(orders)}개")
            print("\n테스트 계정:")
            print("- 관리자: admin / admin123")
            print("- 사용자: user1 / user123")
            print("- 사용자: user2 / user123")
            
            return True
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"테스트 데이터 생성 실패: {e}")
        print(f"❌ 오류 발생: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 