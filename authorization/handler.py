import uuid

from database import get_db_session
from sqlmodel import select
from model import User

from datetime import datetime,timedelta

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

def authenticate_user(username: str):
        user = get_user(username)
        if not user:
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

def get_user(username: str):
    with get_db_session() as session:
        statement = select(User).where(User.username == username)
        return  session.exec(statement).one_or_none()

async def get_current_user(token: str = Header()):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, jwt_key, algorithms=[jwt_alorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user