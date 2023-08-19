from fastapi import APIRouter
from pydantic import BaseModel
from authorization.handler import Token
from service.user import UserService
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

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