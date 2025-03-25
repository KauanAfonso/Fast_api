function consumir_api(api){
    fetch(api)
    .then((resposta)=>resposta.json())
    .then((data)=>console.log(data))
}

consumir_api('http://127.0.0.1:8000/filmes/')