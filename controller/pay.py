import uuid
from fastapi import APIRouter, Body, Depends, Query
from dependency.label import get_user_by_nfc_serial
from model import User

from service.pay import PayService

router = APIRouter(
    prefix="/pay",
    tags=["pay"],
    dependencies=[],
)

@router.post("/nfc/{amount}")
async def pay_nfc(amount:int, user: User = Depends(get_user_by_nfc_serial)):
    return await PayService.pay_nfc(user, amount)

@router.delete("/nfc")
async def pay_post(user: User = Depends(get_user_by_nfc_serial)):
    return await PayService.pay_post(user)



