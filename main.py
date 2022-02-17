from curses.ascii import HT
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select


class ContactBase(SQLModel):
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: Optional[str] = Field(default=None)
    street_number: Optional[str] = Field(default=None)
    street_name: Optional[str] = Field(default=None)
    suburb: Optional[str] = Field(default=None)
    postcode: Optional[str] = Field(default=None)


class Contact(ContactBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ContactCreate(ContactBase):
    pass


class ContactRead(ContactBase):
    id: int


class ContactUpdate(SQLModel):
    first_name: str = None
    last_name: str = None
    email: Optional[str] = None
    street_number: Optional[str] = None
    street_name: Optional[str] = None
    suburb: Optional[str] = None
    postcode: Optional[str] = None


sqlite_file_name = "crc_sqlite.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


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
