"""
테스트 데이터 초기화 스크립트
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.base import SessionLocal, engine, Base
from app.models.menu import Category, Menu

# 테이블 생성
Base.metadata.create_all(bind=engine)

# 세션 생성
db = SessionLocal()

# 기존 데이터 삭제 (옵션)
db.query(Menu).delete()
db.query(Category).delete()

# 카테고리 생성
categories_data = [
    {"name": "커피", "display_order": 1},
    {"name": "논커피", "display_order": 2},
    {"name": "디저트", "display_order": 3},
    {"name": "베이커리", "display_order": 4},
]

categories = {}
for cat_data in categories_data:
    category = Category(**cat_data)
    db.add(category)
    db.commit()
    db.refresh(category)
    categories[cat_data["name"]] = category

# 메뉴 생성
menus_data = [
    # 커피
    {
        "name": "아메리카노",
        "category_id": categories["커피"].id,
        "price": 4500,
        "description": "진한 에스프레소와 뜨거운 물의 조화",
        "image_url": "/images/americano.jpg",
        "is_available": True
    },
    {
        "name": "카페라떼",
        "category_id": categories["커피"].id,
        "price": 5000,
        "description": "부드러운 우유와 에스프레소의 완벽한 밸런스",
        "image_url": "/images/latte.jpg",
        "is_available": True
    },
    {
        "name": "카푸치노",
        "category_id": categories["커피"].id,
        "price": 5000,
        "description": "풍성한 우유 거품과 에스프레소",
        "image_url": "/images/cappuccino.jpg",
        "is_available": True
    },
    {
        "name": "바닐라 라떼",
        "category_id": categories["커피"].id,
        "price": 5500,
        "description": "달콤한 바닐라 시럽이 들어간 카페라떼",
        "image_url": "/images/vanilla-latte.jpg",
        "is_available": True
    },
    
    # 논커피
    {
        "name": "녹차라떼",
        "category_id": categories["논커피"].id,
        "price": 5500,
        "description": "고급 녹차 파우더로 만든 건강한 라떼",
        "image_url": "/images/green-tea-latte.jpg",
        "is_available": True
    },
    {
        "name": "초코라떼",
        "category_id": categories["논커피"].id,
        "price": 5500,
        "description": "진한 초콜릿과 우유의 달콤한 만남",
        "image_url": "/images/choco-latte.jpg",
        "is_available": True
    },
    {
        "name": "레모네이드",
        "category_id": categories["논커피"].id,
        "price": 6000,
        "description": "상큼한 레몬으로 만든 시원한 음료",
        "image_url": "/images/lemonade.jpg",
        "is_available": True
    },
    
    # 디저트
    {
        "name": "티라미수",
        "category_id": categories["디저트"].id,
        "price": 6500,
        "description": "이탈리아 정통 디저트",
        "image_url": "/images/tiramisu.jpg",
        "is_available": True
    },
    {
        "name": "치즈케이크",
        "category_id": categories["디저트"].id,
        "price": 6000,
        "description": "부드럽고 진한 뉴욕 스타일 치즈케이크",
        "image_url": "/images/cheesecake.jpg",
        "is_available": False  # 품절 예시
    },
    
    # 베이커리
    {
        "name": "크로와상",
        "category_id": categories["베이커리"].id,
        "price": 3500,
        "description": "버터 향이 가득한 프랑스 정통 크로와상",
        "image_url": "/images/croissant.jpg",
        "is_available": True
    },
    {
        "name": "베이글",
        "category_id": categories["베이커리"].id,
        "price": 3000,
        "description": "쫄깃한 플레인 베이글",
        "image_url": "/images/bagel.jpg",
        "is_available": True
    },
]

for menu_data in menus_data:
    menu = Menu(**menu_data)
    db.add(menu)

db.commit()
db.close()

print("✅ 테스트 데이터가 성공적으로 추가되었습니다!")
print(f"   - 카테고리: {len(categories)}개")
print(f"   - 메뉴: {len(menus_data)}개") 