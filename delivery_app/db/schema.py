from typing import Optional
from pydantic import EmailStr
from datetime import datetime
from delivery_app.db.models import StatusChoicess, OrderStatusChoicess, CourierStatusChoicess
from pydantic import BaseModel


class UserProfileSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    hashed_password: str
    email: EmailStr
    phone_number: Optional[str] = None
    profile_image: Optional[str] = None
    age: Optional[int] = None
    status: StatusChoicess
    date_registered: datetime


class CategorySchema(BaseModel):
    id: int
    category_name: str


class StoreSchema(BaseModel):
    id: int
    store_name: str
    description: str
    store_image: str
    address: str
    category_id: int
    owner_id: int


class ContactSchema(BaseModel):
    id: int
    title: str
    contact_number: Optional[str] = None
    social_network: Optional[str] = None
    store_id: int


class ProductSchema(BaseModel):
    id: int
    product_name: str
    description: str
    product_image: str
    price: float
    store_id: int


class ComboSchema(BaseModel):
    id: int
    combo_name: str
    description: str
    combo_image: str
    price: float
    store_id: int


class OrderSchema(BaseModel):
    id: int
    client_id: int
    order_status: OrderStatusChoicess
    delivery_address: str
    courier_id: int
    created_at: datetime


class CourierSchema(BaseModel):
    id: int
    courier_id: int
    order_id: int
    courier_status: CourierStatusChoicess


class StoreReviewSchema(BaseModel):
    id: int
    client_id: int
    store_id: int
    text: Optional[str] = None
    stars: Optional[int] = None
    created_date: datetime


class CourierRatingSchema(BaseModel):
    id: int
    client_id: int
    courier_id: int
    rating: int
    created_date: datetime














