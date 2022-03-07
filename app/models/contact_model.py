from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class PhoneBase(SQLModel):
    desc: str = Field(index=True)
    number: int = Field(index=False)
    contact_id: Optional[int] = Field(default=None, foreign_key="contact.id")


class Phone(PhoneBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    contact: "Contact" = Relationship(back_populates="phones")


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
    phones: List["Phone"] = Relationship(back_populates="contact")


class ContactCreate(ContactBase):
    pass


class ContactRead(ContactBase):
    id: int
    phones: List[Phone] = []


class ContactUpdate(SQLModel):
    first_name: str = None
    last_name: str = None
    email: Optional[str] = None
    street_number: Optional[str] = None
    street_name: Optional[str] = None
    suburb: Optional[str] = None
    postcode: Optional[str] = None
