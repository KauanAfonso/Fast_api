from .models2 import Base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .models2 import Movies  # Certifique-se de que a classe Movies está importada

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Exemplo de banco SQLite, altere conforme necessário

# Crie a engine e o SessionLocal
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crie todas as tabelas no banco
Base.metadata.create_all(bind=engine)
