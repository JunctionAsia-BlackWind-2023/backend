import uuid
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Union, Optional
import datetime
class User(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    username:   str
    permission: str
    cost: int = Field(default=0)
    label: Optional["Label"] = Relationship(back_populates="user")

class Amusement(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False
    )
    name: str
    labels: List["Label"] = Relationship(back_populates="amusement")

class Label(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    user_id: uuid.UUID = Field(default=None,foreign_key="user.id",nullable=True)
    user: Optional[User] = Relationship(back_populates="label")
    nfc_serial: str 
    physical_id: str # = Field(default=None,foreign_key="physical.id",nullable=False)
    locker_number: int
    # landmark_id: uuid.UUID = Field(default=None,foreign_key="Landmark.id",nullable=True)
    amusement_id: Optional[uuid.UUID] = Field(default=None, foreign_key="amusement.id", nullable=True)
    amusement: Optional[Amusement] = Relationship(back_populates="labels")
    wait_time: Optional[datetime.datetime] = Field(default=None, nullable=True)
    bright_time: Optional[datetime.datetime] = Field(default=None, nullable=True)
    location: Union[str, None]

class Event(SQLModel, table=True):
    iid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    name: str
    location: str
    start_time: datetime.datetime

class Landmark(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    location: str
    name:     str