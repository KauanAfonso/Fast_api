from core.configs import settings
from sqlalchemy import Column, Integer, String, Boolean, Float

class LocalModel(settings.DBBaseModel):
    __tablename__ = "locais"
    
    id: int = Column(Integer(), primary_key=True, autoincrement=True)
    nome: str = Column(String(255))
    relacao: str = Column(String(255))
    foto: str = Column(String(255))