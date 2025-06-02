'''
Esse arquivo ficará toda a configuração
do nosso codigo

'''

from pydantic.v1 import BaseSettings 
from sqlalchemy.orm import declarative_base

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    # API_V2_STR  Se tivesse outras versões da api...
    DB_URL: str = "mysql+asyncmy://root@127.0.0.1:3306/profissoes" #conexão do banco
    DBBaseModel = declarative_base() #Trabalhar com bancos de dados relacionais de forma orientada a objetos (ORM — Object Relational Mapper).

#Arquivos de config 
class Config:
    case_sensitive = False
    env_file = "../env"


settings = Settings() #defindo minha classe na varivel settings