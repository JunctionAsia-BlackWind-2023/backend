from base64 import b64decode
from datetime import timedelta

from fastapi import HTTPException,status
from sqlmodel import select
from passlib.context import CryptContext

from model import User

from database import get_db_session

from util.crypto import decrypt, encrypt, verify_password,get_password_hash

from secret import access_token_expire_minutes


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    async def register_user(name: str,student_id: int,password: str,email: str):
        user = User(name=name,student_id=student_id,password=password,email=email)

        with get_db_session() as session:
            statement = select(User).where(User.email == user.email)
            results = session.exec(statement)
            if results.one_or_none() != None:
                raise HTTPException(status_code=400, detail="The email is already signed up.")


        with get_db_session() as session:
            session.add(user)
            session.commit()

        return {"message": "email has been sent"}

    async def verify_user(id: str,nonce:str,tag:str):
        id = b64decode(id)
        nonce = b64decode(nonce)
        tag = b64decode(tag)

        decrypted_id = decrypt(nonce,id,tag)

        with get_db_session() as session:
            statement = select(User).where(User.id == decrypted_id)
            results = session.exec(statement)
            user = results.one()
            user.verified = True
            session.add(user)
            session.commit()

        return {"message": "your account has been successfully created."}

    