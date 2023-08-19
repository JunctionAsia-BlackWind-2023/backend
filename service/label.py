from fastapi import HTTPException
from sqlmodel import select
from database import get_db_session
from model import Label


class LabelService:
    async def register_label(physical_id: str, nfc_serial:str, locker_number: int):
        label = Label(physical_id=physical_id, nfc_serial=nfc_serial, locker_number=locker_number)

        with get_db_session() as session:
            statement = select(Label).where(Label.physical_id == label.physical_id or Label.nfc_serial == label.nfc_serial or Label.locker_number == label.locker_number)
            results = session.exec(statement)
            if results.one_or_none() is not None:
                raise HTTPException(status_code=400, detail="The label is already signed up.")


        with get_db_session() as session:
            session.add(label)
            session.commit()

        return label
