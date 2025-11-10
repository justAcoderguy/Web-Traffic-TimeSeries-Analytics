import sqlmodel
from sqlmodel import SQLModel, Session
from api.db.config import DATABASE_URL, DATABASE_TZ
import timescaledb

if DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL needs to be set")

engine = timescaledb.create_engine(DATABASE_URL, DATABASE_TZ)


def init_db():
    print("creating db")
    SQLModel.metadata.create_all(engine)
    print("creating hypertables")
    timescaledb.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session