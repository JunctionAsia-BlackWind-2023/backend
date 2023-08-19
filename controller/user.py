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
    name: str
    student_id: int
    password: str
    email: str

class LoginRequestParam(BaseModel):
    email: str
    password: str

@router.post("/signup")
async def register_user(param : RegisterParam):
    return await UserService.register_user(param.name,param.student_id,param.password,param.email)

@router.get("/signup/verify")
async def verify_user(id:str,nonce:str,tag:str):
    return await UserService.verify_user(id,nonce,tag)

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: LoginRequestParam):
    return await UserService.login(form_data.email,form_data.password)