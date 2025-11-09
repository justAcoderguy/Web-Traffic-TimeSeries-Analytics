from fastapi import APIRouter, Depends, HTTPException
from api.db.session import get_session
from sqlmodel import Session, select

from .models import (
    EventModel, 
    EventListSchema,
    EventCreateSchema,
    EventUpdateSchema
)

router = APIRouter()

@router.get("/")
def read_events(sess: Session = Depends(get_session)) -> EventListSchema:
    query = select(EventModel).order_by(EventModel.id.asc()).limit(10)
    results = sess.exec(query).all()
    return {
        "results": results, # returning List[EventModel]
        "count": len(results)
    }

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


@router.put("/{event_data}")
def update_event(
        event_id: int, 
        payload:EventUpdateSchema, 
        sess: Session = Depends(get_session)
    ) -> EventModel:
    # Can only update the description
    query = select(EventModel).where(EventModel.id == event_id)
    row = sess.exec(query).first()
    if not row:
        raise HTTPException(status_code=404, detail="Event not found")
    
    data = payload.model_dump()
    for k, v in data.items():
        setattr(row, k, v)

    sess.add(row)
    sess.commit()
    sess.refresh(row)
    return row