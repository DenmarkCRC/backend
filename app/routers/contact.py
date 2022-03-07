from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select
from ..models.contact_model import (
    ContactRead,
    Contact,
    ContactUpdate,
    ContactCreate,
    Phone,
)
from ..database import get_session

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.get("/", response_model=List[ContactRead])
# @router.get("/")
def read_contacts(*, session: Session = Depends(get_session)):
    # statement = select(Contact, Phone).where(Phone.contact_id == Contact.id)
    # contacts = session.exec(statement).all()
    contacts = session.exec(select(Contact)).all()
    return contacts


@router.get("/{contact_id}", response_model=ContactRead)
def read_contact(*, session: Session = Depends(get_session), contact_id: int):
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.patch("/{contact_id}", response_model=ContactRead)
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


@router.post("/", response_model=ContactRead)
def create_contact(*, session: Session = Depends(get_session), contact: ContactCreate):
    db_contact = Contact.from_orm(contact)
    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)
    return db_contact


@router.delete("/{contact_id}")
def delete_contact(*, session: Session = Depends(get_session), contact_id: int):
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    session.delete(contact)
    session.commit()
    return {"ok": True}
