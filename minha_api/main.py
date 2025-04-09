from fastapi import FastAPI, Response, status, Depends, HTTPException
from .models2 import Movies
from sqlalchemy.orm import Session
from .schema import Filme_Model
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from . import database

app = FastAPI()

origins = [
    "http://localhost",  # Permitir localhost
    "http://127.0.0.1:5500",   # ip do server_front
      
]

#Permitir outros acessos 'pingar' na api
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir origens que você especificou
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos HTTP
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)


#função para obter uma sessãodo banco de dados
def get_db():
    db = database.SessionLocal()
    try: 
        yield db
    finally:
        db.close()


#Root da api
@app.get('/')
def retornar_root():
    return{'Uma API feita por': 'Kauan Afonso😎'}

# #Filtrar filme por nome do filme com query paramters
# @app.get('/filmes/', status_code=200)
# def pesquisar_filme(response: Response, nome_filme: str | None = None):
#     if nome_filme:
#         for i in filmes.values():
#             if i['nome'].lower() == nome_filme.lower():
#                 return{"Filme": i}
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {'erro': 'filme não encontrado'}
#     return{"Filmes": filmes}


# #Retornar todos os filmes
# @app.get('/filmes/', status_code=200)
# def retornar_todos():
#     return filmes

# #Filtrar filme por id
# @app.get('/filmes/{id_filme}', status_code=200)
# def retornar_filme(id_filme:int, response:Response):
#     if id_filme in filmes:
#         return filmes[id_filme]
#     response.status_code = status.HTTP_404_NOT_FOUND
#     return {'erro': 'filme não encontrado'}

#Criar um filme
@app.post('/filmes/', response_model=Filme_Model)
def criar_filme(movie: Filme_Model, db: Session = Depends(get_db)): 
    db_movie = Movies(name=movie.name, director=movie.director, year=movie.year, gender=movie.gender, actors=movie.actors, ratings=movie.ratings)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

# #Atualizar um filme
# @app.put('/filmes/{id_filme}', status_code=200)
# async def atualiar_filme(id_filme:int, filme_atualizado: Filme_Model, response:Response):
#     if id_filme in filmes:
#         filmes[id_filme] = filme_atualizado
#         return{'Filme atualizado com sucesso': filme_atualizado}
#     else:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return{'erro': "Filme não encontrado"}

# #Deletar um filme
# @app.delete('/filmes/{id_filme}', status_code=200)
# async def excluir_filme(id_filme:int, response:Response):
#     if id_filme in filmes:
#         filme_excluido = filmes[id_filme] #Armazenando o filme excluido para printar ele ao usuario
#         del filmes[id_filme]
#         return{'Mensagem':'Filme excluido com sucesso', "Filme excluído: ":filme_excluido}
#     else:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return{'erro': 'filme não encontrado!'}


# # uvicorn main:app --reload --host 10.234.94.98 --port 8000 -> Definir host e porta 