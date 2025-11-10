from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from typing import List, Optional
from timescaledb import TimescaleModel # for timescale hypertables

import sqlmodel


class EventModel(TimescaleModel, table=True):
    page: str = Field(index=True)
    description: Optional[str] = ""
    # Below two are provided as PK by timescaledb as default

    # id: Optional[int] = Field(default=None, primary_key=True)

    # created_at: datetime = Field(
    #     default_factory=get_utc,
    #     sa_type=sqlmodel.DateTime(timezone=True),
    #     nullable=False
    # ) 

    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 4 months"


class EventCreateSchema(TimescaleModel):
    page: str
    description: Optional[str] = Field(default="")


class EventUpdateSchema(TimescaleModel):
    description: str


class EventListSchema(TimescaleModel):
    results: List[EventModel]
    count: int

    


