from fastapi import FastAPI
from app.database import Base, engine
from app.routers import savings

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Savings Tracker API")

app.include_router(savings.router)
