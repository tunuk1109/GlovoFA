from fastapi import FastAPI
from delivery_app.db.database import SessionLocal
import redis.asyncio as redis
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter
from delivery_app.api.endpoints import (auth, categories, combo, contact, courier,
                                        order, product, rating, review, Stors)
from delivery_app.admin.setup import setup_admin
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from delivery_app.config import SECRET_KEY


async def init_redis():
    return redis.Redis.from_url('redis://localhost', encoding='utf-8', decode_responses=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await init_redis()
    await FastAPILimiter.init(redis)
    yield
    await redis.close()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


delivery_app = FastAPI(title='Glovo Site', lifespan=lifespan)
delivery_app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
setup_admin(delivery_app)


delivery_app.include_router(auth.auth_router)
delivery_app.include_router(categories.category_router)
delivery_app.include_router(Stors.store_router)
delivery_app.include_router(contact.contact_router)
delivery_app.include_router(product.product_router)
delivery_app.include_router(combo.combo_router)
delivery_app.include_router(order.order_router)
delivery_app.include_router(courier.courier_router)
delivery_app.include_router(review.review_router)
delivery_app.include_router(rating.rating_router)


if __name__ == '__main__':
    uvicorn.run(delivery_app, host='127.0.0.1', port=8000)






























