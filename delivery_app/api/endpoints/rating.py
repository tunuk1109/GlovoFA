from delivery_app.db.schema import CourierRatingSchema
from delivery_app.db.models import CourierRating
from delivery_app.db.database import SessionLocal
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter


rating_router = APIRouter(prefix='/rating', tags=['Ratings'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@rating_router.post('/', response_model=CourierRatingSchema)
async def rating_create(rating: CourierRatingSchema, db: Session = Depends(get_db)):
    rating_db = CourierRating(**rating.dict())
    db.add(rating_db)
    db.commit()
    db.refresh(rating_db)
    return rating_db


@rating_router.get('/', response_model=List[CourierRatingSchema])
async def rating_list(db: Session = Depends(get_db)):
    rating_db = db.query(CourierRating).all()
    return rating_db


@rating_router.get('/{rating_id}/', response_model=CourierRatingSchema)
async def rating_detail(rating_id: int, db: Session = Depends(get_db)):
    rating_db = db.query(CourierRating).filter(CourierRating.id == rating_id).first()
    if rating_db is None:
        raise HTTPException(status_code=404, detail='Information not found')
    return rating_db


@rating_router.put('/{rating_id}/', response_model=CourierRatingSchema)
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


@rating_router.delete('/{rating_id}/')
async def rating_delete(rating_id: int, db: Session = Depends(get_db)):
    rating_db = db.query(CourierRating).filter(CourierRating.id == rating_id).first()
    if rating_db is None:
        raise HTTPException(status_code=404, detail='Information not found')

    db.delete(rating_db)
    db.commit()
    return {'message': 'This rating is deleted'}
