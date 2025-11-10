from fastapi import APIRouter, Depends, HTTPException, Query
from api.db.session import get_session
from sqlmodel import Session, select
from sqlalchemy import func, case
from datetime import datetime, timedelta, timezone
from timescaledb.hyperfunctions import time_bucket

from typing import List

from .models import (
    EventModel, 
    EventBucketSchema,
    EventCreateSchema,
)

router = APIRouter()

DEFAULT_LOOKUP_PAGES = [
        "/", "/about", "/pricing", "/contact", 
        "/blog", "/products", "/login", "/signup",
        "/dashboard", "/settings"
    ]

@router.get("/")
def read_events(
        duration: str = Query(default="1 day"),
        pages: List = Query(default=None),
        sess: Session = Depends(get_session)
    ) -> List[EventBucketSchema]:

    os_case = case(
        (EventModel.user_agent.ilike('%windows%'), 'Windows'),
        (EventModel.user_agent.ilike('%macintosh%'), 'MacOS'),
        (EventModel.user_agent.ilike('%iphone%'), 'iOS'),
        (EventModel.user_agent.ilike('%android%'), 'Android'),
        (EventModel.user_agent.ilike('%linux%'), 'Linux'),
        else_='Other'
    ).label('operating_system')

    bucket = time_bucket(duration, EventModel.time)
    lookup_pages = pages if isinstance(pages, list) and len(pages) > 0 else DEFAULT_LOOKUP_PAGES
    query = (
        select(
            bucket.label('bucket'),
            os_case,
            EventModel.page.label('page'),
            func.avg(EventModel.duration).label("avg_duration"),
            func.count().label('count')
        )
        .where(
            EventModel.page.in_(lookup_pages)
        )
        .group_by(
            bucket,
            os_case,
            EventModel.page,
        )
        .order_by(
            bucket,
            os_case,
            EventModel.page,
        )
    )
    results = sess.exec(query).fetchall()
    return results

@router.post("/")
def create_event(
        payload: EventCreateSchema, 
        sess: Session = Depends(get_session)
    ) -> EventModel:
    data = payload.model_dump() # payload (json) -> pydantic_model -> dict ( model_dump )
    row = EventModel.model_validate(data)
    sess.add(row)
    sess.commit()
    sess.refresh(row) # relod this objects data ( to get id and stuff )
    return row

  
@router.get("/{event_id}")
def get_event(event_id: int, sess: Session = Depends(get_session)) -> EventModel:
    query = select(EventModel).where(EventModel.id == event_id)
    result = sess.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    return result
