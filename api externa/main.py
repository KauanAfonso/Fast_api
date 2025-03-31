from fastapi import FastAPI
import requests

app = FastAPI()

#Função que consome a api
def buscar_cep_api(cep):
    return requests.get(f'https://viacep.com.br/ws/{cep}/json/').json()

#Acessar com minha 
@app.get('/buscar/cep/{cep}')
def buscar_cep(cep:int):
    cep_local = buscar_cep_api(cep)
    return {"Cep buscado:": cep_local}