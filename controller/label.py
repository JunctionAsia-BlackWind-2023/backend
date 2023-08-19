from fastapi import APIRouter
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

