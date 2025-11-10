from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from typing import List, Optional
from timescaledb import TimescaleModel # for timescale hypertables

import sqlmodel


class EventModel(TimescaleModel, table=True):
    page: str = Field(index=True)
    user_agent: Optional[str] = Field(default="", index=True) # browser
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True) 
    session_id: Optional[str] = Field(index=True)
    duration: Optional[int] = Field(default=0) 

    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 4 months"


class EventCreateSchema(TimescaleModel):
    page: str
    user_agent: Optional[str] = Field(default="", index=True) # browser
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True) 
    session_id: Optional[str] = Field(index=True)
    duration: Optional[int] = Field(default=0) 



class EventBucketSchema(TimescaleModel):
    bucket: datetime
    page: str
    ua: Optional[str] = ""
    operating_system: Optional[str] = "" # infering from ua ( user_agent )
    avg_duration: Optional[float] = 0.0
    count: int
    


