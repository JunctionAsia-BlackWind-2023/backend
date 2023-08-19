import datetime
import uuid
from fastapi import HTTPException

from sqlmodel import select
from database import get_db_session
from infra.ESL import broadcast_img

from model import Event


class EventService:
    async def create_event(name: str, location: str, start_time: datetime.datetime):
        event = Event(name=name, location=location, start_time=start_time)

        with get_db_session() as session:
            session.add(event)
            session.commit()
            session.refresh(event)
            return event
        
    async def get_eventlist():
        with get_db_session() as session:
            statement = select(Event)
            events = session.exec(statement).all()

            return events

    async def broadcast(event_id: uuid.UUID):
        with get_db_session() as session:
            e_statement = select(Event).where(Event.id == event_id)
            event = session.exec(e_statement).one_or_none()

            if event is not None:
                raise HTTPException(status_code=404, detail="This event doesn't exist.")
            
            broadcast_img()

            return
