from fastapi import HTTPException
from sqlmodel import select
from database import get_db_session
from model import Label, User

async def get_label(locker_number:int):
    with get_db_session() as session:
        statement = select(Label).where(Label.locker_number==locker_number)
        return session.exec(statement).one_or_none()

async def get_user_by_nfc_serial(nfc_serial: str):
    with get_db_session() as session:
        statement = select(User,Label).where(Label.nfc_serial == nfc_serial).join(User)
        user = session.exec(statement).one_or_none()

        if user is not None:
            raise HTTPException(status_code=400, detail="This label is not matched with user.")
        
        return user
