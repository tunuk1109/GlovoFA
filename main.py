from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Category, Store, Contact, Product, Combo, Order, Courier, StoreReview, CourierRating
from schema import (CategorySchema, StoreSchema, ContactSchema, ProductSchema, StoreReviewSchema,
                    ComboSchema, OrderSchema, CourierSchema, CourierRatingSchema)
from typing import List


delivery_app = FastAPI(title='Glovo Site')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@delivery_app.post('/category/create/', response_model=CategorySchema)
async def category_create(category: CategorySchema, db: Session = Depends(get_db)):

    category_db = Category(category_name=category.category_name)
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db


@delivery_app.get('/category/', response_model=List[CategorySchema])
async def category_list(db: Session = Depends(get_db)):
    return db.query(Category).all()


@delivery_app.get('/category/{category_id}', response_model=CategorySchema)
async def category_detail(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id==category_id).first()
    if category is None:
        raise HTTPException(status_code=400, detail='Category is not found')
    return category


@delivery_app.put('/category/{category_id}', response_model=CategorySchema)
async def category_update(category_id: int, category: CategorySchema,
                          db: Session = Depends(get_db)):

    category_db = db.query(Category).filter(Category.id==category_id).first()
    if category_db is None:
        raise HTTPException(status_code=400, detail='Category is not found')

    category_db.category_name = category.category_name
    db.add(category_db)
    db.commit()
    db.refresh(category_db)

    return category_db


@delivery_app.delete('/category/{category_id}')
async def category_delete(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if category_db is None:
        raise HTTPException(status_code=400, detail='Category is not found')

    db.delete(category_db)
    db.commit()
    return {'message': 'This category is deleted'}


@delivery_app.post('/store/create/', response_model=StoreSchema)
async def store_create(store: StoreSchema, db: Session = Depends(get_db)):
    store_db = Store(**store.dict())
    db.add(store_db)
    db.commit()
    db.refresh(store_db)
    return store_db


@delivery_app.get('/store/', response_model=List[StoreSchema])
async def store_list(db: Session = Depends(get_db)):
    return db.query(Store).all()


@delivery_app.get('/store/{store_id}/', response_model=StoreSchema)
async def store_detail(store_id: int, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if store_db is None:
        raise HTTPException(status_code=404, detail='Information not found')
    return store_db


@delivery_app.put('/store/{store_id}/', response_model=StoreSchema)
async def store_update(store_id: int, store: StoreSchema, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if store_db is None:
        raise HTTPException(status_code=404, detail='Information not fount')

    for store_key, store_value in store.dict().items():
        setattr(store_db, store_key, store_value)

    db.add(store_db)
    db.commit()
    db.refresh(store_db)
    return store_db


@delivery_app.delete('/store/{store_id}/')
async def store_delete(store_id: int, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if store_db is None:
        raise HTTPException(status_code=404, detail='Information not found')

    db.delete(store_db)
    db.commit()
    return {'message': 'This Store is deleted'}


@delivery_app.post('/contact/create/', response_model=ContactSchema)
async def contact_create(contact: ContactSchema, db: Session = Depends(get_db)):
    contact_db = Contact(**contact.dict())
    db.add(contact_db)
    db.commit()
    db.refresh(contact_db)
    return contact_db


@delivery_app.get('/contact/', response_model=List[ContactSchema])
async def contact_list(db: Session = Depends(get_db)):
    return db.query(Contact).all()


@delivery_app.get('/contact/{contact_id}/', response_model=ContactSchema)
async def contact_detail(contact_id: int, db: Session = Depends(get_db)):
    contact_db = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact_db is None:
        raise HTTPException(status_code=404, detail='Contact not found')

    return contact_db


@delivery_app.put('/contact/{contact_id}/', response_model=ContactSchema)
async def contact_update(contact_id: int, contact: ContactSchema, db: Session = Depends(get_db)):
    contact_db = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact_db is None:
        raise HTTPException(status_code=404, detail='Contact not found')

    for contact_key, contact_value in contact.dict().items():
        setattr(contact_db, contact_key, contact_value)

    db.add(contact_db)
    db.commit()
    db.refresh(contact_db)
    return contact_db


@delivery_app.delete('/contact/{contact_id}/')
async def contact_delete(contact_id: int, db: Session = Depends(get_db)):
    contact_db = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact_db is None:
        raise HTTPException(status_code=404, detail='Contact not found')

    db.delete(contact_db)
    db.commit()
    return {'message': 'This contact is deleted'}


@delivery_app.post('/product/create/', response_model=ProductSchema)
async def product_create(product: ProductSchema, db: Session = Depends(get_db)):
    product_db = Product(**product.dict())

    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@delivery_app.get('/product/', response_model=List[ProductSchema])
async def product_list(db: Session = Depends(get_db)):
    return db.query(Product).all()


@delivery_app.get('/product/{product_id}/', response_model=ProductSchema)
async def product_detail(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if product_db is None:
        raise HTTPException(status_code=404, detail='Product not found')

    return product_db


@delivery_app.put('/product/{product_id}/', response_model=ProductSchema)
async def product_update(product_id: int, product: ProductSchema, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if product_db is None:
        raise HTTPException(status_code=404, detail='Product not found')

    for product_key, product_value in product.dict().items():
        setattr(product_db, product_key, product_value)

    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@delivery_app.delete('/product/{product_id}/')
async def product_delete(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if product_db is None:
        raise HTTPException(status_code=404, detail='Product not found')

    db.delete(product_db)
    db.commit()
    return {'message': 'This product is deleted'}


@delivery_app.post('/combo/create/', response_model=ComboSchema)
async def combo_create(combo: ComboSchema, db: Session = Depends(get_db)):
    combo_db = Combo(**combo.dict())
    db.add(combo_db)
    db.commit()
    db.refresh(combo_db)
    return combo_db


@delivery_app.get('/combo/', response_model=List[ComboSchema])
async def combo_list(db: Session = Depends(get_db)):
    return db.query(Combo).all()


@delivery_app.get('/combo/{combo_id}/', response_model=ComboSchema)
async def combo_detail(combo_id: int, db: Session = Depends(get_db)):
    combo_db = db.query(Combo).filter(Combo.id == combo_id).first()
    if combo_db is None:
        raise HTTPException(status_code=404, detail='Information not found')

    return combo_db


@delivery_app.put('/combo/{combo_id}/', response_model=ComboSchema)
async def combo_update(combo_id: int, combo: ComboSchema, db: Session = Depends(get_db)):
    combo_db = db.query(Combo).filter(Combo.id == combo_id).first()
    if combo_db is None:
        raise HTTPException(status_code=404, detail='Information not found')

    for combo_key, combo_value in combo.dict().items():
        setattr(combo_db, combo_key, combo_value)

    db.add(combo_db)
    db.commit()
    db.refresh(combo_db)
    return combo_db


@delivery_app.delete('/combo/{combo_id}/')
async def combo_delete(combo_id: int, db: Session = Depends(get_db)):
    combo_db = db.query(Combo).filter(Combo.id == combo_id).first()
    if combo_db is None:
        raise HTTPException(status_code=404, detail='Information not found')

    db.delete(combo_db)
    db.commit()
    return {'message': 'This combo is deleted'}


@delivery_app.post('/order/create/', response_model=OrderSchema)
async def order_create(order: OrderSchema, db: Session = Depends(get_db)):
    order_db = Order(**order.dict())

    db.add(order_db)
    db.commit()
    db.refresh(order_db)
    return order_db


@delivery_app.get('/order/', response_model=List[OrderSchema])
async def order_list(db: Session = Depends(get_db)):
    return db.query(Order).all()


@delivery_app.get('/order/{order_id}/', response_model=OrderSchema)
async def order_detail(order_id: int, db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id == order_id).first()
    if order_db is None:
        raise HTTPException(status_code=404, detail='Order not found')

    return order_db


@delivery_app.put('/order/{order_id}/', response_model=OrderSchema)
async def order_update(order_id: int, order: OrderSchema, db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id == order_id).first()
    if order_db is None:
        raise HTTPException(status_code=404, detail='Order not found')

    for order_key, order_value in order.dict().items():
        setattr(order_db, order_key, order_value)

        db.add(order_db)
        db.commit()
        db.refresh(order_db)
        return order_db


@delivery_app.delete('/order/{order_id}/')
async def order_delete(order_id: int, db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id == order_id).first()
    if order_db is None:
        raise HTTPException(status_code=404, detail='Order not found')

    db.delete(order_db)
    db.commit()
    return {'message': 'This order id deleted'}


@delivery_app.post('/courier/create/', response_model=CourierSchema)
async def courier_create(courier: CourierSchema, db: Session = Depends(get_db)):
    courier_db = Courier(**courier.dict())

    db.add(courier_db)
    db.commit()
    db.refresh(courier_db)
    return courier_db


@delivery_app.get('/courier/', response_model=List[CourierSchema])
async def courier_list(db: Session = Depends(get_db)):
    courier_db = db.query(Courier).all()
    return courier_db


@delivery_app.get('/courier/{courier_id}/', response_model=CourierSchema)
async def courier_detail(courier_id: int, db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if courier_db is None:
        raise HTTPException(status_code=404, detail='Courier not found')
    return courier_db


@delivery_app.put('/courier/{courier_id}/', response_model=CourierSchema)
async def courier_update(courier_id: int, courier: CourierSchema, db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if courier_db is None:
        raise HTTPException(status_code=404, detail='Courier not found')

    for courier_key, courier_value in courier.dict().items():
        setattr(courier_db, courier_key, courier_value)

    db.add(courier_db)
    db.commit()
    db.refresh(courier_db)
    return courier_db


@delivery_app.delete('/courier/{courier_id}/')
async def courier_delete(courier_id: int, db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if courier_db is None:
        raise HTTPException(status_code=404, detail='Courier not found')

    db.delete(courier_db)
    db.commit()
    return {'message': 'This courier is deleted'}


@delivery_app.post('/review/create/', response_model=StoreReviewSchema)
async def review_create(review: StoreReviewSchema, db: Session = Depends(get_db)):
    review_db = StoreReview(**review.dict())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db


@delivery_app.get('/review/', response_model=List[StoreReviewSchema])
async def review_list(db: Session = Depends(get_db)):
    review_db = db.query(StoreReview).all()
    return review_db


@delivery_app.get('/review/{review_id/', response_model=StoreReviewSchema)
async def review_detail(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(StoreReview).filter(StoreReview.id == review_id).first()
    if review_db is None:
        raise HTTPException(status_code=404, detail='Information not found')
    return review_db


@delivery_app.put('/review/{review_id}/', response_model=StoreReviewSchema)
async def review_update(review_id: int, review: StoreReviewSchema, db: Session = Depends(get_db)):
    review_db = db.query(StoreReview).filter(StoreReview.id == review_id).first()
    if review_db is None:
        raise HTTPException(status_code=404, detail='Information not found')

    for review_key, review_value in review.dict().items():
        setattr(review_db, review_key, review_value)

    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db


@delivery_app.delete('/review/{review_id}/')
async def review_delete(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(StoreReview).filter(StoreReview.id == review_id).first()
    if review_db is None:
        raise HTTPException(status_code=404, detail='Information not found')

    db.delete(review_db)
    db.commit()
    return {'message': 'This review is deleted'}


@delivery_app.post('/rating/create/', response_model=CourierRatingSchema)
async def rating_create(rating: CourierRatingSchema, db: Session = Depends(get_db)):
    rating_db = CourierRating(**rating.dict())
    db.add(rating_db)
    db.commit()
    db.refresh(rating_db)
    return rating_db


@delivery_app.get('/rating/', response_model=List[CourierRatingSchema])
async def rating_list(db: Session = Depends(get_db)):
    rating_db = db.query(CourierRating).all()
    return rating_db


@delivery_app.get('/rating/{rating_id}/', response_model=CourierRatingSchema)
async def rating_detail(rating_id: int, db: Session = Depends(get_db)):
    rating_db = db.query(CourierRating).filter(CourierRating.id == rating_id).first()
    if rating_db is None:
        raise HTTPException(status_code=404, detail='Information not found')
    return rating_db


@delivery_app.put('/rating/{rating_id}/', response_model=CourierRatingSchema)
async def rating_update(rating_id: int, rating: CourierRatingSchema, db: Session = Depends(get_db)):
    rating_db = db.query(CourierRating).filter(CourierRating.id == rating_id).first()
    if rating_db is None:
        raise HTTPException(status_code=404, detail='Information not found')

    for rating_key, rating_value in rating.dict().items():
        setattr(rating_db, rating_key, rating_value)

    db.add(rating_db)
    db.commit()
    db.refresh(rating_db)
    return rating_db


@delivery_app.delete('/rating/{rating_id}/')
async def rating_delete(rating_id: int, db: Session = Depends(get_db)):
    rating_db = db.query(CourierRating).filter(CourierRating.id == rating_id).first()
    if rating_db is None:
        raise HTTPException(status_code=404, detail='Information not found')

    db.delete(rating_db)
    db.commit()
    return {'message': 'This rating is deleted'}























