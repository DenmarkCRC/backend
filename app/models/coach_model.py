from typing import Optional
from sqlmodel import Field, SQLModel


class CoachBase(SQLModel):
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    hourly_rate: Optional[str] = Field(default=None)
    areas: Optional[str] = Field(default=None)


class Coach(CoachBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class CoachCreate(CoachBase):
    pass


class CoachRead(CoachBase):
    id: int
