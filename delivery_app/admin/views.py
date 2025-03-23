from delivery_app.db.models import (UserProfile, Category, Store, Contact, Product,
                                    Combo, Order, StoreReview, CourierRating, Courier)
from sqladmin import ModelView



class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username, UserProfile.status]
    name = 'User'
    name_plural = 'Users'

class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]
    name = 'Category'
    name_plural = 'Categories'

class StoreAdmin(ModelView, model=Store):
    column_list = [Store.store_name, Store.category]

class ContactAdmin(ModelView, model=Contact):
    column_list = [Contact.store, Contact.contact_number]

class ProductAdmin(ModelView, model=Product):
    column_list = [Product.product_name, Product.price]

class ComboAdmin(ModelView, model=Combo):
    column_list = [Combo.combo_name, Combo.price]

class OrderAdmin(ModelView, model=Order):
    column_list = [Order.client, Order.order_status]

class StoreReviewAdmin(ModelView, model=StoreReview):
    column_list = [StoreReview.client_review, StoreReview.store_review]

class CourierRatingAdmin(ModelView, model=CourierRating):
    column_list = [CourierRating.client_rating, CourierRating.courier_rating, CourierRating.rating]

class CourierAdmin(ModelView, model=Courier):
    column_list = [Courier.courier_id, Courier.courier_status]