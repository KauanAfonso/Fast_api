from pydantic import BaseModel
from typing import List

class Filme_Model(BaseModel):
    name: str
    director: str
    year: int
    gender: str
    actors: str
    ratings: float  # Alterando de str para float

    class Config:
        orm_mode = True 