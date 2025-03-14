from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from models import StatusChoicess, OrderStatusChoicess, CourierStatusChoicess
from pydantic import BaseModel


class UserProfileSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    phone_number: str
    profile_image: Optional[str]
    age: Optional[int]
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
    contact_number: Optional[str]
    social_network: Optional[str]
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
    text: str
    stars: int
    created_date: datetime


class CourierRatingSchema(BaseModel):
    id: int
    client_id: int
    courier_id: int
    rating: int
    created_date: datetime














