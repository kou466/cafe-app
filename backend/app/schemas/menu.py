from pydantic import BaseModel
from typing import Optional, List

# 카테고리 스키마
class CategoryBase(BaseModel):
    name: str
    display_order: int = 0

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    display_order: Optional[int] = None

class Category(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

# 메뉴 스키마
class MenuBase(BaseModel):
    name: str
    category_id: int
    price: int
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_available: bool = True

class MenuCreate(MenuBase):
    pass

class MenuUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None

class Menu(MenuBase):
    id: int
    category: Optional[Category] = None
    
    class Config:
        from_attributes = True 