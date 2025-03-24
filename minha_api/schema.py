from pydantic import BaseModel
from typing import List

class Filme_Model(BaseModel):
    nome: str
    diretor: str
    ano: str
    atores: List[str]
    classificacao: str