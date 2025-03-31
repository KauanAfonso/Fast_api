from typing import Union

from fastapi import FastAPI

app = FastAPI()

#@app -> é um decorador, ou seja ele ira pegar a função de baixo e retorna-la como um função para o fastapai
@app.get("/kauan")
async def read_root(): #aync dispara coisas com tempo independentes
    return {"Hello": "World"}

@app.post("/kauan")
async def read_root():
    return {"message": "Post criado"}

#path parameters
@app.get("/items/{item_id}")
async def read_item(item_id:int):#tipando o argumento
    return {"item_id": item_id}#retornando o argumento

#tipo de enum
from enum import Enum
class ModelName(str,Enum):
    sp = "1"
    rj = '2'
    mg = '3'
    es = '4'

#Pesquisando pelo enum
@app.get("/states/{state_id}")
async def read_state(state_id:ModelName):
    if state_id.value == "1":
        return {"São paulo"}
    if state_id.value == "2":
        return {"Rio de janeiro"}
    if state_id.value == "3":
        return {"MInas Gerais"}
    if state_id.value == "4":
        return {"Espirito Santo"}
    


fake_items_db = [

{"item_number": "01"}, 
{"item_number": "02"}, 
{"item_number": "03"},
{"item_number": "04"}, 
{"item_number": "05"}, 
{"item_number": "06"},
{"item_number": "07"}, 
{"item_number": "08"}, 
{"item_number": "09"},
{"item_number": "10"}, 

]


#Query paramters
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.get("/item_name/")
async def item_name(name:str, age: int | None = None, angry: bool = False):
    if age is not None:
        msg = f"My name is {name} and I am {age} years old !"
        return {'message' : msg}
    if angry is not False:
        msg = f"My name is {name} and I am NOT angry! :()"
        return {"message": msg}
    msg = f"My name is {name}"
    return {'msg': msg}