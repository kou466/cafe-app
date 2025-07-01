from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.config import settings
from app.core.logger import logger
from app.db.base import get_db
from app.models.menu import Menu, Category
from app.schemas.menu import Menu as MenuSchema, MenuCreate, MenuUpdate
from app.schemas.menu import Category as CategorySchema, CategoryCreate

router = APIRouter()

# 카테고리 관련 엔드포인트
@router.get("/categories", response_model=List[CategorySchema])
async def get_categories(
    db: Session = Depends(get_db)
):
    """모든 카테고리 조회 (display_order 순서로 정렬)"""
    try:
        categories = db.query(Category).order_by(Category.display_order, Category.id).all()
        logger.info(f"카테고리 {len(categories)}개 조회 완료")
        return categories
    except Exception as e:
        logger.error(f"카테고리 조회 실패: {e}")
        raise HTTPException(status_code=500, detail="카테고리 조회 중 오류가 발생했습니다")

@router.post("/categories", response_model=CategorySchema)
async def create_category(
    category: CategoryCreate, 
    db: Session = Depends(get_db)
):
    """새 카테고리 생성"""
    try:
        # 중복 확인
        existing = db.query(Category).filter(Category.name == category.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="이미 존재하는 카테고리명입니다")
        
        db_category = Category(**category.dict())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        
        logger.info(f"새 카테고리 생성: {db_category.name} (ID: {db_category.id})")
        return db_category
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"카테고리 생성 실패: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="카테고리 생성 중 오류가 발생했습니다")

# 메뉴 관련 엔드포인트
@router.get("/menus", response_model=List[MenuSchema])
async def get_menus(
    category_id: Optional[int] = Query(None, description="카테고리 ID로 필터링"),
    available_only: bool = Query(True, description="판매 가능한 메뉴만 조회"),
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(
        settings.DEFAULT_PAGE_SIZE, 
        ge=1, 
        le=settings.MAX_PAGE_SIZE, 
        description="조회할 개수"
    ),
    db: Session = Depends(get_db)
):
    """메뉴 목록 조회 (카테고리별 필터링, 페이지네이션 지원)"""
    try:
        query = db.query(Menu)
        
        # 카테고리 필터링
        if category_id:
            query = query.filter(Menu.category_id == category_id)
        
        # 판매 가능 여부 필터링
        if available_only:
            query = query.filter(Menu.is_available == True)
        
        # 페이지네이션 적용
        menus = query.offset(skip).limit(limit).all()
        
        logger.info(f"메뉴 조회: 카테고리={category_id}, 개수={len(menus)}")
        return menus
        
    except Exception as e:
        logger.error(f"메뉴 목록 조회 실패: {e}")
        raise HTTPException(status_code=500, detail="메뉴 조회 중 오류가 발생했습니다")

@router.get("/menus/{menu_id}", response_model=MenuSchema)
async def get_menu(
    menu_id: int, 
    db: Session = Depends(get_db)
):
    """특정 메뉴 조회"""
    try:
        menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            logger.warning(f"존재하지 않는 메뉴 ID 요청: {menu_id}")
            raise HTTPException(status_code=404, detail="메뉴를 찾을 수 없습니다")
        
        logger.info(f"메뉴 조회: {menu.name} (ID: {menu_id})")
        return menu
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"메뉴 조회 실패 (ID: {menu_id}): {e}")
        raise HTTPException(status_code=500, detail="메뉴 조회 중 오류가 발생했습니다")

@router.post("/menus", response_model=MenuSchema)
async def create_menu(
    menu: MenuCreate, 
    db: Session = Depends(get_db)
):
    """새 메뉴 생성"""
    try:
        # 카테고리 존재 확인
        category = db.query(Category).filter(Category.id == menu.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="유효하지 않은 카테고리 ID입니다")
        
        # 메뉴명 중복 확인 (같은 카테고리 내에서)
        existing = db.query(Menu).filter(
            Menu.name == menu.name, 
            Menu.category_id == menu.category_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="같은 카테고리에 동일한 메뉴명이 존재합니다")
        
        db_menu = Menu(**menu.dict())
        db.add(db_menu)
        db.commit()
        db.refresh(db_menu)
        
        logger.info(f"새 메뉴 생성: {db_menu.name} (ID: {db_menu.id}, 카테고리: {category.name})")
        return db_menu
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"메뉴 생성 실패: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="메뉴 생성 중 오류가 발생했습니다")

@router.put("/menus/{menu_id}", response_model=MenuSchema)
async def update_menu(
    menu_id: int, 
    menu: MenuUpdate, 
    db: Session = Depends(get_db)
):
    """메뉴 수정"""
    try:
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            logger.warning(f"수정할 메뉴를 찾을 수 없음: ID {menu_id}")
            raise HTTPException(status_code=404, detail="메뉴를 찾을 수 없습니다")
        
        # 카테고리 변경 시 유효성 확인
        if menu.category_id and menu.category_id != db_menu.category_id:
            category = db.query(Category).filter(Category.id == menu.category_id).first()
            if not category:
                raise HTTPException(status_code=400, detail="유효하지 않은 카테고리 ID입니다")
        
        # 수정사항 적용
        update_data = menu.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_menu, key, value)
        
        db.commit()
        db.refresh(db_menu)
        
        logger.info(f"메뉴 수정 완료: {db_menu.name} (ID: {menu_id})")
        return db_menu
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"메뉴 수정 실패 (ID: {menu_id}): {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="메뉴 수정 중 오류가 발생했습니다")

@router.delete("/menus/{menu_id}")
async def delete_menu(
    menu_id: int,
    db: Session = Depends(get_db)
):
    """메뉴 삭제"""
    try:
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            logger.warning(f"삭제할 메뉴를 찾을 수 없음: ID {menu_id}")
            raise HTTPException(status_code=404, detail="메뉴를 찾을 수 없습니다")
        
        menu_name = db_menu.name
        db.delete(db_menu)
        db.commit()
        
        logger.info(f"메뉴 삭제 완료: {menu_name} (ID: {menu_id})")
        return {"message": f"메뉴 '{menu_name}'가 성공적으로 삭제되었습니다"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"메뉴 삭제 실패 (ID: {menu_id}): {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="메뉴 삭제 중 오류가 발생했습니다") 