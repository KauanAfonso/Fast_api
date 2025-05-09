from fastapi import FastAPI, Response, status
from .models import filmes
from .schema import Filme_Model
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


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

#Root da api
@app.get('/')
def retornar_root():
    return{'Uma API feita por': 'Kauan Afonso😎'}

#Filtrar filme por nome do filme com query paramters
@app.get('/filmes/', status_code=200)
def pesquisar_filme(response: Response, nome_filme: str | None = None):
    if nome_filme:
        for i in filmes.values():
            if i['nome'].lower() == nome_filme.lower():
                return{"Filme": i}
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'erro': 'filme não encontrado'}
    return{"Filmes": filmes}


#Retornar todos os filmes
@app.get('/filmes/', status_code=200)
def retornar_todos():
    return filmes

#Filtrar filme por id
@app.get('/filmes/{id_filme}', status_code =200)
def retornar_filme(id_filme:int, response:Response):
    if id_filme in filmes:
        return filmes[id_filme]
    response.status_code = status.HTTP_404_NOT_FOUND
    return {'erro': 'filme não encontrado'}

#Criar um filme
@app.post('/filmes/')
def criar_filme(filme: Filme_Model):
    
    #Aqui estou pegando a ultima posicao do dicionario
    ultima_chave_dic = list(filmes.keys())[-1]
    nova_posicao = int(ultima_chave_dic) +1 #Na nova posição é a ultima somada + 1
    filmes[nova_posicao] = filme #nova poscicao recebe o novo filme pasado pelo body()

    return {"Filme criado": filme}

#Atualizar um filme
@app.put('/filmes/{id_filme}', status_code=200)
async def atualiar_filme(id_filme:int, filme_atualizado: Filme_Model, response:Response):
    if id_filme in filmes:
        filmes[id_filme] = filme_atualizado
        return{'Filme atualizado com sucesso': filme_atualizado}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return{'erro': "Filme não encontrado"}

#Deletar um filme
@app.delete('/filmes/{id_filme}', status_code=200)
async def excluir_filme(id_filme:int, response:Response):
    if id_filme in filmes:
        filme_excluido = filmes[id_filme] #Armazenando o filme excluido para printar ele ao usuario
        del filmes[id_filme]
        return{'Mensagem':'Filme excluido com sucesso', "Filme excluído: ":filme_excluido}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return{'erro': 'filme não encontrado!'}


# uvicorn main:app --reload --host 10.234.94.98 --port 8000 -> Definir host e porta 