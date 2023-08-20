import uuid
from fastapi import APIRouter, Query
from pydantic import BaseModel
from service.label import LabelService

router = APIRouter(
    prefix="/label",
    tags=["label"],
    dependencies=[],
)
    
class RegisterLabelDTO(BaseModel):
    physical_id: str
    nfc_serial: str
    locker_number: int

@router.post("/")
async def register_label(param : RegisterLabelDTO):
    return await LabelService.register_label(param.physical_id,param.nfc_serial, param.locker_number)

@router.get("/")
async def get_labels():
    return await LabelService.get_labels()

@router.patch("/{label_id}")
async def find_label(label_id: uuid.UUID):
    return await LabelService.find_label(label_id)