from fastapi import HTTPException
from database import get_db_session
from model import User


class PayService:
    async def pay_nfc(user: User, amount: int):
        if amount < 0 :
            raise HTTPException(status_code=400, detail="This amount is invalid cost.")
        
        with get_db_session() as session:
            
            user.User.cost += amount

            session.add(user.User)
            session.commit()
            session.refresh(user.User)

            return user

            return user
    async def pay_post(user: User):
        with get_db_session() as session:
            user.User.cost = 0

            session.add(user.User)
            session.commit()
            session.refresh(user.User)
            return user