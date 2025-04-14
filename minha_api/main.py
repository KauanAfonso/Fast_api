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


#função para obter uma sessão do banco de dados
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


#Criar um filme
@app.post('/filmes/', response_model=Filme_Model)
def create_movie(movie: Filme_Model, db: Session = Depends(get_db)): 
    db_movie = Movies(name=movie.name, director=movie.director, year=movie.year, gender=movie.gender, actors=movie.actors, ratings=movie.ratings)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.get('/filmes/')
def get_movies(db:Session = Depends(get_db)):
    data = db.query(Movies).all()#Pegando tudo
    return data


@app.get('/filmes/{id}', status_code=status.HTTP_200_OK)
def get_movies_id(id:int, response:Response, db:Session = Depends(get_db)):
    try:
        data = db.query(Movies).get(id)
        if data is not None:
            return data
    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'erro': 'filme não encontrado'}
    