from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select
from ..models.coach_model import *
from ..database import get_session

router = APIRouter(prefix="/coaches", tags=["Coaches"])


@router.get("/", response_model=List[CoachRead])
def read_coaches(*, session: Session = Depends(get_session)):
    coaches = session.exec(select(Coach)).all()
    return coaches


@router.post("/", response_model=CoachRead)
def create_coach(*, session: Session = Depends(get_session), coach: CoachCreate):
    db_coach = Coach.from_orm(coach)
    session.add(db_coach)
    session.commit()
    session.refresh(db_coach)
    return db_coach
