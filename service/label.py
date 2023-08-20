import datetime
import uuid
from fastapi import HTTPException
from sqlmodel import select
from database import get_db_session
from infra.ESL import broadcast_img, get_token, set_display_page, trans_img_to_base64, turn_on_LED
from model import Label
from service.dto.labelList import LabelItemDTO


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
            session.refresh(label)

        return label
    async def get_labels():
        with get_db_session() as session:
            labels_statement = select(Label)
            labels = session.exec(labels_statement).all()

            return [LabelItemDTO(label_id=l.id, label_physical_id=l.physical_id, locker_number=l.locker_number, cost= None if l.user is None else l.user.cost) for l in labels]
            

    async def find_label(label_id: uuid.UUID):
        with get_db_session() as session:
            statement = select(Label).where(Label.id == label_id)
            label = session.exec(statement).one_or_none()

            if label is None:
                raise HTTPException(status_code=404, detail="The label doesn't exist.")
            
            token = get_token()
            broadcast_img(
                img_base64=trans_img_to_base64("./resource/ESL-alert.png"),
                ESL_token_type=token["token_type"],
                ESL_token=token["access_token"],
                label_codes=[label.physical_number],
                front_page=3,
                page_index=3,
                )

            set_display_page(
                ESL_token_type=token["token_type"],    
                ESL_token=token["access_token"],
                label_codes=[label.physical_number],
                page_index=3,
            )
                
            turn_on_LED(
                ESL_token_type=token["token_type"],
                ESL_token=token["access_token"],
                label_code=label.physical_id,
                duration="10s"
                )
        
            label.bright_time = datetime.datetime.utcnow()
            session.add(label)
            session.commit()
            session.refresh(label)
            return label

