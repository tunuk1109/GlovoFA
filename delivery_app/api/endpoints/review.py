from delivery_app.db.schema import StoreReviewSchema
from delivery_app.db.models import StoreReview
from delivery_app.db.database import SessionLocal
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter


review_router = APIRouter(prefix='/review', tags=['Reviews'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@review_router.post('/', response_model=StoreReviewSchema)
async def review_create(review: StoreReviewSchema, db: Session = Depends(get_db)):
    review_db = StoreReview(**review.dict())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db


@review_router.get('/', response_model=List[StoreReviewSchema])
async def review_list(db: Session = Depends(get_db)):
    review_db = db.query(StoreReview).all()
    return review_db


@review_router.get('/{review_id/', response_model=StoreReviewSchema)
async def review_detail(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(StoreReview).filter(StoreReview.id == review_id).first()
    if review_db is None:
        raise HTTPException(status_code=404, detail='Information not found')
    return review_db


@review_router.put('/{review_id}/', response_model=StoreReviewSchema)
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


@review_router.delete('/{review_id}/')
async def review_delete(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(StoreReview).filter(StoreReview.id == review_id).first()
    if review_db is None:
        raise HTTPException(status_code=404, detail='Information not found')

    db.delete(review_db)
    db.commit()
    return {'message': 'This review is deleted'}