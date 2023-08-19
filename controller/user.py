import uuid
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dependency.auth import Token, get_current_user
from dependency.label import get_label, get_user_by_nfc_serial
from model import Label, User
from service.user import UserService
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

class RegisterParam(BaseModel):
    username: str
    permission: str

class LoginRequestParam(BaseModel):
    username: str
    

@router.post("/signup")
async def register_user(param : RegisterParam):
    return await UserService.register_user(param.username,param.permission)

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: LoginRequestParam):
    return await UserService.login(form_data.username)

class MatchingLabelDTO(BaseModel):
    locker_number: int

@router.post("/:id/label")
async def match_label(user: User = Depends(get_current_user),label: Label = Depends(get_label)):
    return await UserService.match_label(user, label)

@router.delete("/:id/label")
async def unmatch_label(user: User = Depends(get_user_by_nfc_serial)):
    return await UserService.unmatch_label(user)