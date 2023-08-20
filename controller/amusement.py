import uuid
from fastapi import APIRouter, Body, Depends, Query
from dependency.auth import get_current_user
from model import User
from service.amusement import AmusementService

router = APIRouter(
    prefix="/amusement",
    tags=["amusement"],
    dependencies=[],
)


@router.post("/")
async def register_amusement(name:str):
    return await AmusementService.register_amusement(name)

@router.post("/{amusement_id}")
async def wait_amusement(amusement_id: uuid.UUID, nfc_serial: str =  Body()):
    return await AmusementService.wait_amusement(amusement_id, nfc_serial)

@router.patch("/{amusement_id}")
async def take_out_entry(amusement_id: uuid.UUID, num_entries:int = Body()):
    return await AmusementService.take_out_entry(amusement_id, num_entries)

@router.get("/{amusement_id}/count")
async def count_waiting(amusement_id: uuid.UUID, user: User = Depends(get_current_user)):
    return await AmusementService.count_waiting(amusement_id, user)