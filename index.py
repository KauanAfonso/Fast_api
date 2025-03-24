from fastapi import FastAPI
from typing import Union
from enum import Enum
from pydantic import BaseModel

'''
parametros da url
'''

app = FastAPI()

@app.get("/")
def read_root():
    return {"hello": "world"}

@app.get("/items/{item_id}")
async def read_item(item_id:int):#tipando o argumento
    return {"item_id": item_id}#retornando o argumento


'''
A ordem importa, caso a func 
02 fosse declarada primeiro
a 01 não funcionaria, pois
ela se concidiriam

'''
#01
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

#02
@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}


#enum
class ModelName(str, Enum):
    kauan = "kauan"
    cris = "cris"
    pedro = "pedro"

#A req só ira funcionar se o nome estiver em
#odelNome
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name.value == "kauan":
        return {"modelName": model_name, "message": "vai corinthians"}
    if model_name.value == 'cris':
        return{"modelName": model_name, "message":"Sou eu aqui"}
    

#parametros consulta

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items_total/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit] #filtrando por skip e limit


#copo da requisição
class Item(BaseModel):
    name:str
    description:Union[str, None] = None #parametro opcional
    price:float


@app.post("/items/criar")
async def create_item(item: Item):
    return {'item_created': item}

#ele ira atualizar o corpo da requisição com um id 
#passado pela req e adicionar esse id na Item
@app.put('/items/{item_id}')
async def uptade_item(item_id:int, item:Item):
    return {'item_id': item_id, **item.dict()}