from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.order import OrderStatus

# 주문 아이템 스키마
class OrderItemBase(BaseModel):
    menu_id: int
    quantity: int = Field(..., gt=0, description="수량은 1 이상이어야 합니다")
    options: Optional[str] = Field(None, max_length=200, description="옵션 (예: 샷 추가, 얼음 적게)")

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)
    options: Optional[str] = Field(None, max_length=200)

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    price: int
    subtotal: int
    
    class Config:
        from_attributes = True

# 주문 스키마
class OrderBase(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=50)
    customer_phone: str = Field(..., min_length=10, max_length=20)
    pickup_time: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=500)

class OrderCreate(OrderBase):
    items: List[OrderItemCreate] = Field(..., min_items=1, description="최소 1개 이상의 메뉴가 필요합니다")

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    customer_name: Optional[str] = Field(None, min_length=2, max_length=50)
    customer_phone: Optional[str] = Field(None, min_length=10, max_length=20)
    pickup_time: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=500)

class Order(OrderBase):
    id: int
    user_id: Optional[int] = None
    total_amount: int
    status: OrderStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    order_items: List[OrderItem] = []
    
    class Config:
        from_attributes = True

# 주문 생성 응답 스키마
class OrderCreateResponse(BaseModel):
    order: Order
    message: str = "주문이 성공적으로 생성되었습니다"

# 주문 목록 조회용 간단한 스키마
class OrderSummary(BaseModel):
    id: int
    customer_name: str
    customer_phone: str
    total_amount: int
    status: OrderStatus
    created_at: datetime
    item_count: int
    
    class Config:
        from_attributes = True 