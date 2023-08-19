import uuid
from fastapi import HTTPException
import datetime
from sqlalchemy import update
from sqlmodel import select
from database import get_db_session
from model import Amusement, Label, User
from service.dto.amusement import CountWaitingDTO

class AmusementService:
    async def register_amusement(name: str):
        amusement = Amusement(name=name)

        with get_db_session() as session:
            session.add(amusement)
            session.commit()
            session.refresh(amusement)

        return amusement
    
    async def wait_amusement(amusement_id: uuid.UUID, nfc_serial: str):
        with get_db_session() as session:
            label_statement = select(Label).where(Label.nfc_serial == nfc_serial)
            amuse_statement = select(Amusement).where(Amusement.id == amusement_id)

            label = session.exec(label_statement).one_or_none()
            amuse = session.exec(amuse_statement).one_or_none()

            if label is None:
                raise HTTPException(status_code=400, detail="The label doesn't exist.")
            if amuse is None:
                raise HTTPException(status_code=404, detail="The label doesn't exist.")
            
            amuse.labels.append(label)
            label.wait_time = datetime.datetime.utcnow()
            session.add(amuse)
            session.commit()
            session.refresh(amuse)

            return amuse
        
    async def take_out_entry(amusedment_id: uuid.UUID, num_entries: int):
        with get_db_session() as session:
            amuse_statement = select(Amusement).where(Amusement.id==amusedment_id)
            amuse = session.exec(amuse_statement).one_or_none()

            if amuse is None:
                raise HTTPException(status_code=400, detail="The amusement doesn't exist.")
            
            labels_statement = select(Label).where(Label.amusement_id == amuse.id).limit(num_entries).order_by(Label.wait_time)
            results = session.exec  (labels_statement).all()

            for r in results:
                r.wait_time = None
                r.amusement_id = None
                session.add(r)

            session.commit()
            session.refresh(amuse)
            return amuse
        
    async def count_waiting(amusedment_id: uuid.UUID, user_id: uuid.UUID):
        with get_db_session() as session:
            statement = select(User,Label).join(Label).where(User.id == user_id)
            label = session.exec(statement).one_or_none()
            
            if label is None:
                raise HTTPException(status_code=400, detail="The amusement doesn't exist.")
            
            infront_statement = select(Label).where(Label.amusement_id == amusedment_id and Label.wait_time < label.wait_time)
            results = session.exec(infront_statement).all()

            return CountWaitingDTO(count=len(results)) 

