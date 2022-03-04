from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .models import *
from .database import engine, create_db_and_tables
from .routers import contact, coach

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contact.router)
app.include_router(coach.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "Hello New World!!!"}
