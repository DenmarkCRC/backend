from typing import Optional

from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Contact(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: str
    street_number: str
    street_name: str
    suburb: str
    postcode: str



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


@app.post("/contacts/")
def create_contact(contact: Contact):
    with Session(engine) as session:
        session.add(contact)
        session.commit()
        session.refresh(contact)
        return contact


@app.get("/contacts/")
def read_contacts():
    with Session(engine) as session:
        contacts = session.exec(select(Contact)).all()
        return contacts