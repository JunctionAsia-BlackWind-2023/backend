from fastapi import HTTPException
from database import get_db_session
from model import User


class PayService:
    async def pay_nfc(user: User, amount: int):
        if amount < 0 :
            raise HTTPException(status_code=400, detail="This amount is invalid cost.")
        
        with get_db_session() as session:
            user.cost += amount

            session.add(user)
            session.commit()
            session.refresh(user)

            return user
    async def pay_post(user: User):
        with get_db_session() as session:
            user.cost = 0

            session.add(user)
            session.commit()
            session.refresh(user)
            return user