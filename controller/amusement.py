import uuid
from fastapi import APIRouter
from service.amusement import AmusementService

router = APIRouter(
    prefix="/amusement",
    tags=["amusement"],
    dependencies=[],
)


@router.post("/")
async def register_amusement(name:str):
    return await AmusementService.register_amusement(name)


@router.post("/:id")
async def wait_amusement(amusement_id: uuid.UUID, nfc_serial: str):
    return await AmusementService.wait_amusement(amusement_id, nfc_serial)