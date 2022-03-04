from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from models import *
from database import *


def get_session():
    with Session(engine) as session:
        yield session


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


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# contacts
@app.get("/contacts/", response_model=List[ContactRead])
def read_contacts(*, session: Session = Depends(get_session)):
    contacts = session.exec(select(Contact)).all()
    return contacts


@app.get("/contacts/{contact_id}", response_model=ContactRead)
def read_contact(*, session: Session = Depends(get_session), contact_id: int):
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@app.patch("/contacts/{contact_id}", response_model=ContactRead)
def update_contact(
    *, session: Session = Depends(get_session), contact_id: int, contact: ContactUpdate
):
    db_contact = session.get(Contact, contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact_data = contact.dict(exclude_unset=True)
    for key, value in contact_data.items():
        setattr(db_contact, key, value)
    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)
    return db_contact


@app.post("/contacts/", response_model=ContactRead)
def create_contact(*, session: Session = Depends(get_session), contact: ContactCreate):
    db_contact = Contact.from_orm(contact)
    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)
    return db_contact


@app.delete("/contacts/{contact_id}")
def delete_contact(*, session: Session = Depends(get_session), contact_id: int):
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    session.delete(contact)
    session.commit()
    return {"ok": True}


# coaches


@app.get("/coaches", response_model=List[CoachRead])
def read_coaches(*, session: Session = Depends(get_session)):
    coaches = session.exec(select(Coach)).all()
    return coaches


@app.post("/coaches", response_model=CoachRead)
def create_coach(*, session: Session = Depends(get_session), coach: CoachCreate):
    db_coach = Coach.from_orm(coach)
    session.add(db_coach)
    session.commit()
    session.refresh(db_coach)
    return db_coach
