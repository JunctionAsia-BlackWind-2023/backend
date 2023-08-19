from database import get_db_session
from sqlmodel import select
from model import User

from datetime import datetime,timedelta
from util.crypto import verify_password

from secret import jwt_key,jwt_alorithm

from fastapi import Depends,HTTPException, status,Header

from jose import JWTError, jwt

from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

from typing import Union

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Union[str, None]

def authenticate_user(email: str, password: str):
        user = get_user(email)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        if user.verified == 0: 
            return False
        return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None]):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_key, algorithm=jwt_alorithm)
    return encoded_jwt

def get_user(email: str):
    with get_db_session() as session:
        statement = select(User).where(User.email == email)
        return  session.exec(statement).one_or_none()

async def get_current_user(token: str = Header()):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, jwt_key, algorithms=[jwt_alorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user