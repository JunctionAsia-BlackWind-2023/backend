from typing import Optional
import uuid

from pydantic import BaseModel

class LabelItemDTO(BaseModel):
    label_id: uuid.UUID
    label_physical_id: str
    locker_number: int
    cost: Optional[int]
    