from core.configs import settings
from sqlalchemy import Column, Integer, String, Boolean, Float

#Modelo de profissao
class ProfissaoModel(settings.DBBaseModel):
    __tablename__ = "profissao"
    
    id: int = Column(Integer(), primary_key=True, autoincrement=True)
    nome: str = Column(String(255))
    area: str = Column(String(255))
    formacao: str = Column(String(255))
    salario: float = Column(Float())
    foto: str = Column(String(255))