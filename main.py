from database import create_db_and_tables
from fastapi import Depends, FastAPI, HTTPException, status

from model import *

from controller import user

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():

    return {"message": "Hello World"}

app.include_router(user.router,prefix="/api/v1",)