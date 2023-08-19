import uuid
from fastapi import APIRouter, Body, Depends
from dependency.label import get_user_by_nfc_serial
from model import User

from service.pay import PayService

router = APIRouter(
    prefix="/pay",
    tags=["pay"],
    dependencies=[],
)

@router.post("/nfc")
async def pay_nfc(user: User = Depends(get_user_by_nfc_serial), amount:int = Body()):
    return await PayService.pay_nfc(user, amount)

@router.patch("/nfc")
async def pay_post(user: User = Depends(get_user_by_nfc_serial)):
    return await PayService.pay_post(user)



