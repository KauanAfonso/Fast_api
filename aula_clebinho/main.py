from typing import Union

from fastapi import FastAPI

app = FastAPI()



'''
#@app -> é um decorador, ou seja ele ira pegar a função de baixo e retorna-la como um função para o fastapai
@app.get("/")
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


#----------------------------------------------Query paramters
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

from typing import Union
from pydantic import BaseModel


#---------------------------------------Usando o Base model
class Item(BaseModel):
    name : str
    description : Union[str, None] = None #ou será str ou none, e se ele não mandar nada será none
    price: float
    tax: Union[float,None] = None


@app.post('/items/')
async def create_item(item:Item):
    print(item.model_dump)
    return item


# @app.put('/curso/{curso_id}')
# asyn

class Curso(BaseModel):
    name:str
    duration:int

@app.put('/curso/{curso_id}')
async def update_curso(curso_id: int, curso: Curso):
    return{"curso_id": curso_id, **curso.model_dump()}




#---------------------------------QUERY PARAMTERS

#Função de query 
from fastapi import Query

@app.get("/items_query/")
# Define um endpoint GET acessível na rota "/items_query/"
async def read_items(
    q: Union[str, None] = Query(
        default=None,                     # O parâmetro é opcional (None por padrão)
        max_length=50,                    # Tamanho máximo da string: 50 caracteres
        min_length=3,                     # Tamanho mínimo da string: 3 caracteres
        title="Titulo do item",           # Título do parâmetro na documentação automática (Swagger)
        description="Descrição sobre o item deve ser STR",  # Descrição na documentação
        deprecated=False,                  # Indica que esse parâmetro está obsoleto (aparece tachado na docs)
        pattern="^[^\W\d_]{3}$"         # Expressão regular para validar o valor do parâmetro (⚠️ Tem um erro aqui)
    )
):
    
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q}) #adicionou o q no results
    return results
   

#enviando varios valores
@app.get("/mulitple_items/")
async def read_items(q: list[str] | None = Query(default=None, title="Valor de Consulta nulo", description="Olá eu sou a descricao")):
    query_items = {'q':q}
    return query_items #ex:http://127.0.0.1:8000/items/?q=Kauan&q=joao



from typing import Annotated

#query parameters com parametros default
@app.get("/items_default/")
async def read_items(q: Annotated[list[str], Query(max_length=50)] = ['foo', 'baa']): #anonotated força ter mais de um tipo
    query_itens = ({"q": q})
    return query_itens


#-----------------------Parametros de validação númericas


from typing import Annotated

from fastapi import FastAPI, Path

app = FastAPI()


#------------Intervalor de valores
# ge = maior ou igual
#gt = maior que
#le = menor ou igual
#lt = menor que

@app.get("/items_number/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=99, le=67)], q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


'''

'''
#------------modelo de parametris de consulta -> 

from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at" #pode ter um dos dois valores / valor padrao
    tags: list[str] = [] #lista de 


@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query



from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}#Se ele tentar enviar um parametro adicional ->traga essa mensagem

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query




#----------------------------------Parametros de Consulta no body----------
# Parametros diferefentes e um deles vem do corpo
from typing import Annotated

from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    #ou passa como parametro uma string ou um item
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results




#---------------------Multiplos parametros enviando no copor da requisião automatico

from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: int, importance: Annotated[int, Body()] = 0
    ):
    # a variavel importance nesse caso será enviada no corpo da requisição
    results = {
        "item_id": item_id, 
        "importance": importance
        }
    return results




#-----------------------Body fields---------------------
#Seria o msm que o query mas para o corpo da requisição -> ou seja, define o que e como precisa ser enviado!

from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results



#------------------Tipo set -> Um tipo de dado que não te permite repetir valores

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

'''

#-----------------------------------Um dicionario dentro do outro(modelo aninhado) 

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Image(BaseModel):
    url: str
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None #Aqui acontece isso.


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results