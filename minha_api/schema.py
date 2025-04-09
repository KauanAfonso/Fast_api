from pydantic import BaseModel
from typing import List

class Filme_Model(BaseModel):
    name: str
    director: str
    year: int
    gender: str
    actors: str
    ratings: str

    class Config:
        orm_mode = True 