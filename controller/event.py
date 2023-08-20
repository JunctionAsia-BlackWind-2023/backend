import datetime
import uuid
from fastapi import APIRouter, Query
from pydantic import BaseModel
from service.event import EventService

router = APIRouter(
    prefix="/event",
    tags=["event"],
    dependencies=[],
)

class CreateEventDTO(BaseModel):
    name: str
    location: str
    start_time: datetime.datetime

@router.post("/")
async def create_event(param: CreateEventDTO):
    return await create_event(param.name, param.location, param.start_time)

@router.get("/")
async def get_eventlist():
    return await get_eventlist()

@router.post("/{event_id}")
async def broadcast(event_id: uuid.UUID):
    return await EventService.broadcast(event_id)
