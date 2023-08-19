from base64 import b64decode
from datetime import timedelta

from fastapi import HTTPException,status
from sqlmodel import select
from passlib.context import CryptContext
from dependency.auth import create_access_token, authenticate_user

from model import Label, User

from database import get_db_session

from secret import access_token_expire_minutes


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    async def register_user(username: str,permission: str):
        user = User(username=username,permission=permission)

        with get_db_session() as session:
            statement = select(User).where(User.username == user.username)
            results = session.exec(statement)
            if results.one_or_none() != None:
                raise HTTPException(status_code=400, detail="The user is already signed up.")


        with get_db_session() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    async def login(username: str):
        user = authenticate_user(username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )


        access_token_expires = timedelta(minutes=access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    async def match_label(user: User, label:Label):
        with get_db_session() as session:
            label.user_id = user.id
            session.add(label)
            session.commit()
            session.refresh(label)
        
        return label
    