from typing import Optional
from pydantic import BaseModel as SCBaseModel

class LocalSchema(SCBaseModel):
    id: Optional[int] = None
    nome:str
    relacao: str
    foto:str

    class Config:
        orm_mode = True #Serializa os dados