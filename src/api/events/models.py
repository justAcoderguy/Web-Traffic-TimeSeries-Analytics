from sqlmodel import SQLModel, Field
from typing import List, Optional


class EventModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    page: Optional[str] = ""
    description: Optional[str] = ""


class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = Field(default="")


class EventUpdateSchema(SQLModel):
    description: str


class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int

    


