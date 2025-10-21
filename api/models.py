from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class SaleBase(BaseModel):
    """Базовая модель продажи"""
    product_name: str
    amount: float
    quantity: int
    date: datetime
    status: str


class SaleCreate(SaleBase):
    """Модель для создания продажи"""
    pass


class SaleResponse(SaleBase):
    """Модель ответа с продажей"""
    id: int
    user_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    """Базовая модель пользователя"""
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None


class UserCreate(UserBase):
    """Модель для создания пользователя"""
    is_demo: bool = False


class UserResponse(UserBase):
    """Модель ответа с пользователем"""
    id: int
    created_at: datetime
    is_demo: bool

    class Config:
        from_attributes = True


class StatsResponse(BaseModel):
    """Модель статистики"""
    total_amount: float
    total_sales: int
    average_check: float
    completed_sales: int
    pending_sales: int
    cancelled_sales: int
    conversion_rate: float


class ChartDataPoint(BaseModel):
    """Точка данных для графика"""
    date: str
    value: float


class ChartResponse(BaseModel):
    """Модель данных для графиков"""
    labels: List[str]
    values: List[float]


class TopProduct(BaseModel):
    """Топ товар"""
    product_name: str
    total_amount: float
    total_quantity: int
    sales_count: int


class TopProductsResponse(BaseModel):
    """Модель топ товаров"""
    products: List[TopProduct]
