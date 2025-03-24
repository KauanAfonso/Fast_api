from fastapi import FastAPI
from .models import filmes
from .schema import Filme_Model


app = FastAPI()

@app.get('/')
def retornar_todos():
    return filmes

@app.get('/filmes/{id_filme}')
def retornar_filme(id_filme:int):
    if id_filme in filmes:
        return filmes[id_filme]
    return {'erro': 'filme não encontrado'}

@app.post('/filmes/criar')
def criar_filme(filme: Filme_Model):
    ultima_chave_dic = list(filmes.keys())[-1]
    nova_posicao = int(ultima_chave_dic) +1
    filmes[nova_posicao] = filme

    return {"Filme criado": filme}