from sqlalchemy import String, Integer, Enum, DateTime, Float, DECIMAL, Text, ForeignKey
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import datetime, date


class StatusChoicess(str, PyEnum):
    client = 'client'
    owner = 'owner'
    courier = 'courier'


class OrderStatusChoicess(str, PyEnum):
    awaiting_processing = 'awaiting_processing'
    delivered = 'delivered'
    process_of_delivery = 'process_of_delivery'
    cancelled = 'cancelled'


class CourierStatusChoicess(str, PyEnum):
    available = 'available'
    busy = 'busy'


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    profile_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[StatusChoicess] = mapped_column(Enum(StatusChoicess), default='client')
    date_registered: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    owner_store: Mapped[List['Store']] = relationship('Store', back_populates='owner',
                                                      cascade='all, delete-orphan')
    client_order: Mapped[List['Order']] = relationship('Order', back_populates='client', foreign_keys='Order.client_id',
                                                       cascade='all, delete-orphan')
    courier_order: Mapped[List['Order']] = relationship('Order', back_populates='courier', foreign_keys='Order.courier_id',
                                                        cascade='all, delete-orphan')
    courier: Mapped[List['Courier']] = relationship('Courier', back_populates='courier_courier',
                                                    cascade='all, delete-orphan')
    review_client: Mapped[List['StoreReview']] = relationship('StoreReview', back_populates='client_review',
                                                              cascade='all, delete-orphan')
    clients_rating: Mapped[List['CourierRating']] = relationship('CourierRating', back_populates='client_rating', foreign_keys='CourierRating.client_id',
                                                                 cascade='all, delete-orphan')
    rating_courier: Mapped[List['CourierRating']] = relationship('CourierRating', back_populates='courier_rating', foreign_keys='CourierRating.courier_id',
                                                                 cascade='all, delete-orphan')



class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(32), unique=True)
    category_store: Mapped[List['Store']] = relationship('Store', back_populates='category',
                                                         cascade='all, delete-orphan')


class Store(Base):
    __tablename__ = 'store'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_name: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(Text)
    store_image: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String(64))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped['Category'] = relationship('Category', back_populates='category_store')
    owner_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    owner: Mapped['UserProfile'] = relationship('UserProfile', back_populates='owner_store')
    store_contact: Mapped[List['Contact']] = relationship('Contact', back_populates='store',
                                                          cascade='all, delete-orphan')
    products_store: Mapped[List['Product']] = relationship('Product', back_populates='store_product',
                                                          cascade='all, delete-orphan')
    combo_store: Mapped[List['Combo']] = relationship('Combo', back_populates='store_combo',
                                                      cascade='all, delete-orphan')
    review_store: Mapped[List['StoreReview']] = relationship('StoreReview', back_populates='store_review',
                                                             cascade='all, delete-orphan')


class Contact(Base):
    __tablename__ = 'contact'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(64))
    contact_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    social_network: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store: Mapped['Store'] = relationship('Store', back_populates='store_contact')


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(Text)
    product_image: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store_product: Mapped['Store'] = relationship('Store', back_populates='products_store')


class Combo(Base):
    __tablename__ = 'combo'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    combo_name: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(Text)
    combo_image: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store_combo: Mapped['Store'] = relationship('Store', back_populates='combo_store')


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    client: Mapped['UserProfile'] = relationship('UserProfile', back_populates='client_order', foreign_keys=[client_id])
    order_status: Mapped[OrderStatusChoicess] = mapped_column(Enum(OrderStatusChoicess), default='awaiting_processing')
    delivery_address: Mapped[str] = mapped_column(String(128))
    courier_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    courier: Mapped['UserProfile'] = relationship('UserProfile', back_populates='courier_order', foreign_keys=[courier_id])
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    orders: Mapped[List['Courier']] = relationship('Courier', back_populates='current_order',
                                                   cascade='all, delete-orphan')


class Courier(Base):
    __tablename__ = 'courier'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    courier_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    courier_courier: Mapped['UserProfile'] = relationship('UserProfile', back_populates='courier')
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    current_order: Mapped['Order'] = relationship('Order', back_populates='orders')
    courier_status: Mapped[CourierStatusChoicess] = mapped_column(Enum(CourierStatusChoicess), default='available')


class StoreReview(Base):
    __tablename__ = 'store_review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    client_review: Mapped['UserProfile'] = relationship('UserProfile', back_populates='review_client')
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store_review: Mapped['Store'] = relationship('Store', back_populates='review_store')
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    stars: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CourierRating(Base):
    __tablename__ = 'courier_rating'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    client_rating: Mapped['UserProfile'] = relationship('UserProfile', back_populates='clients_rating', foreign_keys=[client_id])
    courier_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    courier_rating: Mapped['UserProfile'] = relationship('UserProfile', back_populates='rating_courier', foreign_keys=[courier_id])
    rating: Mapped[int] = mapped_column(Integer)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)












