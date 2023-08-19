

from pydantic import BaseModel

class CountWaitingDTO(BaseModel):
    count: int