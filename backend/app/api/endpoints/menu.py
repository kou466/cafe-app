from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.models.menu import Menu, Category
from app.schemas.menu import Menu as MenuSchema, MenuCreate, MenuUpdate
from app.schemas.menu import Category as CategorySchema, CategoryCreate

router = APIRouter()

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 카테고리 관련 엔드포인트
@router.get("/categories", response_model=List[CategorySchema])
def get_categories(db: Session = Depends(get_db)):
    """모든 카테고리 조회"""
    return db.query(Category).order_by(Category.display_order).all()

@router.post("/categories", response_model=CategorySchema)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """새 카테고리 생성"""
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# 메뉴 관련 엔드포인트
@router.get("/menus", response_model=List[MenuSchema])
def get_menus(
    category_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """메뉴 목록 조회 (카테고리별 필터링 가능)"""
    query = db.query(Menu)
    if category_id:
        query = query.filter(Menu.category_id == category_id)
    return query.offset(skip).limit(limit).all()

@router.get("/menus/{menu_id}", response_model=MenuSchema)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    """특정 메뉴 조회"""
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="메뉴를 찾을 수 없습니다")
    return menu

@router.post("/menus", response_model=MenuSchema)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    """새 메뉴 생성"""
    db_menu = Menu(**menu.dict())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

@router.put("/menus/{menu_id}", response_model=MenuSchema)
def update_menu(menu_id: int, menu: MenuUpdate, db: Session = Depends(get_db)):
    """메뉴 수정"""
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="메뉴를 찾을 수 없습니다")
    
    for key, value in menu.dict(exclude_unset=True).items():
        setattr(db_menu, key, value)
    
    db.commit()
    db.refresh(db_menu)
    return db_menu 