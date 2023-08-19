import uuid
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    username:   str
    permission: str

class Label(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    user_id:     uuid.UUID = Field(default=None,foreign_key="user.id",nullable=False)
    physical_id: uuid.UUID # = Field(default=None,foreign_key="physical.id",nullable=False)
    landmark_id: uuid.UUID = Field(default=None,foreign_key="landmark.id",nullable=False)
    
    locker_number: str
    location:      str
    
    cost: int
    
class Landmark(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    
    location: str
    name:     str