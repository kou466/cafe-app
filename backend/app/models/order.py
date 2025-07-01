from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Enum, Text
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class OrderStatus(enum.Enum):
    PENDING = "pending"      # 대기중
    CONFIRMED = "confirmed"  # 확인됨
    PREPARING = "preparing"  # 준비중
    READY = "ready"         # 준비완료
    COMPLETED = "completed"  # 완료
    CANCELLED = "cancelled"  # 취소

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # 비회원 주문 허용
    total_amount = Column(Integer)  # 총 금액 (원 단위)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    customer_name = Column(String(50))  # 주문자명
    customer_phone = Column(String(20))  # 연락처
    pickup_time = Column(DateTime)  # 픽업 예정 시간
    notes = Column(Text)  # 요청사항
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 관계 설정
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_id = Column(Integer, ForeignKey("menus.id"))
    quantity = Column(Integer)
    price = Column(Integer)  # 주문 당시 가격
    subtotal = Column(Integer)  # 소계 (quantity * price)
    options = Column(String(200))  # 옵션 (예: 샷 추가, 얼음 적게)
    
    # 관계 설정
    order = relationship("Order", back_populates="order_items")
    menu = relationship("Menu") 