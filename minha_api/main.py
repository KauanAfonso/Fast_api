from fastapi import FastAPI
from .models import filmes
from .schema import Filme_Model


app = FastAPI()


@app.get('/')
def retornar_root():
    return{'Uma API feita por': 'Kauan Afonso😎'}

@app.get('/filmes')
def retornar_todos():
    return filmes

@app.get('/filmes/filtrar/{nome_filme}')
def pesquisar_filme(nome_filme: str):
    for i in filmes:
        if filmes[i]['nome'] == nome_filme:
            return {"Filme":filmes[i]}
    return {'erro': 'filme não encontrado'}


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

@app.put('/filmes/atualizar/{id_filme}')
async def atualiar_filme(id_filme:int, filme_atualizado: Filme_Model):
    if id_filme in filmes:
        filmes[id_filme] = filme_atualizado
        return{'Filme atualizado com sucesso': filme_atualizado}
    else:
        return{'erro': "Filme não encontrado"}
    
@app.delete('/filmes/delete/{id_filme}')
async def excluir_filme(id_filme:int):
    if id_filme in filmes:
        del filmes[id_filme]
        return{'Mensagem','Filme excluido com sucesso'}
    else:
        return{'erro': 'filme não encontrado!'}
