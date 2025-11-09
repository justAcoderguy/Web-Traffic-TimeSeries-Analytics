from contextlib import asynccontextmanager

from fastapi import FastAPI
from api.events.routing import router as event_router
from api.db.session import init_db

# wrapper around the entire lifecycle of app
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    # cleanup

app = FastAPI(lifespan=lifespan)
app.include_router(event_router, prefix="/api/events")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/healthz")
def api_health_check():
    return {"status": "ok"}
