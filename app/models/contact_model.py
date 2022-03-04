from typing import Optional
from sqlmodel import Field, SQLModel


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
