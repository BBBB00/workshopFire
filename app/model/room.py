from typing import Optional, List
from pydantic import BaseModel, Field


class createRoomModel(BaseModel):
    room: str = Field(min_length=4, max_length=4)
    bed_size: str
    cost: int
    status: str


class updateRoomModel(BaseModel):
    bed_size: Optional[str]
    cost: Optional[int]
    status: Optional[str]
