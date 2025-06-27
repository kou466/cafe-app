from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    display_order = Column(Integer, default=0)
    
    # 관계 설정
    menus = relationship("Menu", back_populates="category")

class Menu(Base):
    __tablename__ = "menus"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    price = Column(Integer)
    description = Column(String)
    image_url = Column(String)
    is_available = Column(Boolean, default=True)
    
    # 관계 설정
    category = relationship("Category", back_populates="menus") 