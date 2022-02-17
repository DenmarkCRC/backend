from typing import List, Optional

from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select


class ContactBase(SQLModel):
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: str
    street_number: str
    street_name: str
    suburb: str
    postcode: str


class Contact(ContactBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ContactCreate(ContactBase):
    pass


class ContactRead(ContactBase):
    id: int


sqlite_file_name = "crc_sqlite.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/contacts/", response_model=ContactRead)
def create_contact(contact: ContactCreate):
    with Session(engine) as session:
        db_contact = Contact.from_orm(contact)
        session.add(db_contact)
        session.commit()
        session.refresh(db_contact)
        return db_contact


@app.get("/contacts/", response_model=List[ContactRead])
def read_contacts():
    with Session(engine) as session:
        contacts = session.exec(select(Contact)).all()
        return contacts
