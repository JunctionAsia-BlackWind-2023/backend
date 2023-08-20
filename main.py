import asyncio
from database import create_db_and_tables
from fastapi import Depends, FastAPI, HTTPException, status

from model import *

from controller import user, label, amusement,pay
from service.amusement import AmusementService
from service.label import LabelService
from service.pay import PayService
from service.user import UserService
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

async def init():
    labels = await asyncio.gather(*[LabelService.register_label('0848A6D2E1D5','02:FE:42:2C:F3:0D:51:A1',523),
    LabelService.register_label('0848A6EEE1DA','02:FE:42:2C:F3:72:24:95',121),
    LabelService.register_label('0848A6E0E1D4','02:FE:42:2C:F3:72:21:8D',247),
    LabelService.register_label('0848A729E1D0','02:FE:42:2C:F3:72:14:8D',712),
    LabelService.register_label('0848A705E1DE','02:FE:42:2C:F3:72:2C:99',483)])

    users = await asyncio.gather(*[UserService.register_user('sangmin', 'admin'),
    UserService.register_user('woojin', 'admin'),
    UserService.register_user('gangmin', 'parent'),
    UserService.register_user("haeyun", "child"),
    UserService.register_user("kyeongmin","child")])

    await UserService.match_label(users[0], labels[0])
    await UserService.match_label(users[1], labels[1])
    await UserService.match_label(users[2], labels[2])
    await UserService.match_label(users[3], labels[3])

    amuses = await asyncio.gather(*[
        AmusementService.register_amusement('Rafting slide'),
        AmusementService.register_amusement('Wild surfing'),
        AmusementService.register_amusement('Jet slide'),
        AmusementService.register_amusement('Racing slide'),
        AmusementService.register_amusement('Tornado slide'),
        AmusementService.register_amusement('Aqua drop')])
    
    await AmusementService.wait_amusement(amuses[0].id, labels[0].nfc_serial)
    await AmusementService.wait_amusement(amuses[1].id, labels[1].nfc_serial)
    await AmusementService.wait_amusement(amuses[0].id, labels[2].nfc_serial)
    await AmusementService.wait_amusement(amuses[0].id, labels[3].nfc_serial)

    count = await AmusementService.count_waiting(amuses[0].id,users[3])
    await AmusementService.take_out_entry(amuses[0].id, 1)

    pay_user = await PayService.pay_nfc(users[0], 1000)
    pay_user = await PayService.pay_nfc(pay_user, 2000)
    pay_user = await PayService.pay_nfc(pay_user, 3000)

    await PayService.pay_post(pay_user)

    await LabelService.turn_on_led(labels[1].id)
    print(labels[0])
    return

@app.on_event("startup")
def on_startup():
    # create_db_and_tables()
    # asyncio.run(init())
    pass

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def suceess():
    create_db_and_tables()
    await init()
    return {"message": "Success"}
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router,prefix="/api/v1",)
app.include_router(label.router, prefix="/api/v1")
app.include_router(amusement.router,prefix="/api/v1")
app.include_router(pay.router, prefix="/api/v1")