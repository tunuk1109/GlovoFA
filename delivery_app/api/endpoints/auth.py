from delivery_app.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, ALGORITHM
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from fastapi_limiter.depends import RateLimiter
from fastapi import  Depends, HTTPException, status, APIRouter
from typing import  Optional
from delivery_app.db.schema import UserProfileSchema
from delivery_app.db.models import UserProfile, RefreshToken
from delivery_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from starlette.requests import Request
from delivery_app.config import settings
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name='github',
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_KEY,
    authorize_url='http://github.com/login/oauth/authorize'
)


auth_router = APIRouter(prefix='/auth', tags=['Authorization'])

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login/')
password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

def veryfi_password(plan_password, hash_password):
    return password_context.verify(plan_password, hash_password)

def get_password_hash(password):
    return password_context.hash(password)


@auth_router.post('/register/')
async def register(user: UserProfileSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    if user_db:
        raise HTTPException(status_code=400, detail='such username already exists')
    new_hash_pass = get_password_hash(user.hashed_password)
    new_user = UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        profile_image=user.profile_image,
        age=user.age,
        status=user.status,
        hashed_password=new_hash_pass
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@auth_router.post('/Login', dependencies = [Depends(RateLimiter(times=3, seconds=200))])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.username == form_data.username).first()
    if not user or not veryfi_password(form_data.password, user.hashed_password):
        return HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Information not right')

    access_token = create_access_token({'sub': user.username})
    refresh_token = create_refresh_token({'sub': user.username})

    token_db = RefreshToken(token=refresh_token, user_id=user.id)
    db.add(token_db)
    db.commit()

    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}


@auth_router.post('/logout/')
async def logout(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

    db.delete(stored_token)
    db.commit()
    return {'message': 'Logged out successfully'}


@auth_router.post('/refresh/')
async def refresh(refresh_token: str, db: Session = Depends(get_db)):
    token_entry = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not token_entry:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')

    new_access_token = create_access_token({'sub': token_entry.user.id})
    return {'access_token': new_access_token, 'token_type': 'bearer'}


@auth_router.get('/github')
async def github_login(request: Request):
    redirect_url = settings.GITHUB_LOGIN_CALLBACK
    return await oauth.github.authorize_redirect(request, redirect_url)























