

import uuid
from pydantic import BaseModel

class CountWaitingDTO(BaseModel):
    count: int

class AmuseDTO(BaseModel):
    name: str
    wait: int
    id: uuid.UUID