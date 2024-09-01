from fastapi import FastAPI,Body
from fastapi.responses import HTMLResponse

# instancia de fastapi
app = FastAPI()

app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Accion"
	},
    {
		"id": 2,
		"title": "Antes de conocerte",
		"overview": "En un pelicula romantica",
		"year": "2019",
		"rating": 8.1,
		"category": "Drama"
	}
]

@app.get('/',tags=['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')

@app.get('/movies',tags=['movies'])
def get_movies():
    return movies

# id es un parameter path
@app.get('/movies/{id}',tags=['movies'])
def get_movie(id:int):
    for item in movies:
        if item["id"] == id:
            return item
    
    return []

# category es un parameter query
@app.get('/movies/',tags=['movies'])
def get_movies_by_category(category:str):
   return [item for item in movies if item["category"] == category]

# para que los campos se han considerados
# como parte del request body y no como variable query 
# es necesario asignarles que son de tipo Body	       
@app.post('/movies',tags=['movies'])
def create_movie(id:int = Body(),title:str=Body(),overview:str=Body(),
                 year:int=Body(),rating:float=Body(),category:str=Body()):
    movies.append({
      "id":id,
      "title":title,
      "overview":overview,
      "year":year,
      "rating":rating,
      "category":category
	})

    return movies


@app.put('/movies/{id}',tags=['movies'])
def update_movie(id:int , title:str=Body(),overview:str=Body(),
                 year:int=Body(),rating:float=Body(),category:str=Body()):
    for item in movies:
        if item["id"] == id:
            item["title"] = title   
            item["overview"] = overview
            item["year"] = year   
            item["rating"] = rating   
            item["year"] = year   
            item["category"] = category

    return movies

@app.delete('/movies/{id}',tags=['movies'])
def delete_movie(id: int): 
    for item in movies:
    	if item["id"] == id:
            movies.remove(item)
            return movies







