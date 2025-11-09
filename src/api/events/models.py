from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from typing import List, Optional

import sqlmodel

def get_utc():
    return datetime.now(timezone.utc)


class EventModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    page: Optional[str] = ""
    description: Optional[str] = ""
    created_at: datetime = Field(
        default_factory=get_utc,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False
    )


class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = Field(default="")


class EventUpdateSchema(SQLModel):
    description: str


class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int

    


