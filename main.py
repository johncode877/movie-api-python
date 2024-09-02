from fastapi import FastAPI,Body,Path,Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel,Field
from typing import Optional


# instancia de fastapi
app = FastAPI()

app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

# clase que hereda de BaseModel 
# pydantic es un modulo
# que permite trabajar con esquemas
class Movie(BaseModel):
    id: Optional[int]=None
    title: str = Field(min_length=5,max_length=15)
    overview: str = Field(min_length=15,max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=1,le=10)
    category: str = Field(min_length=5,max_length=15)
     
    class Config:
        json_schema_extra = {
           "examples" : [
               {
                "id": 1,
                "title": "Mi pelicula",
                "overview": "Descripcion de la pelicula",
                "year": 2022,
                "rating": 9.8,
                "category": "Accion"
               }
            ]
        }
    

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
def get_movie(id:int=Path(ge=1,le=2000)):
    for item in movies:
        if item["id"] == id:
            return item
    
    return []

# category es un parameter query
@app.get('/movies/',tags=['movies'])
def get_movies_by_category(category:str=Query(min_length=5,max_length=15)):
   return [item for item in movies if item["category"] == category]

# para que los campos se han considerados
# como parte del request body y no como variable query 
# es necesario asignarles que son de tipo Body	       
@app.post('/movies',tags=['movies'])
def create_movie(movie:Movie):
    movies.append(movie)

    return movies


@app.put('/movies/{id}',tags=['movies'])
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title   
            item["overview"] = movie.overview
            item["year"] = movie.year   
            item["rating"] = movie.rating   
            item["year"] = movie.year   
            item["category"] = movie.category

    return movies

@app.delete('/movies/{id}',tags=['movies'])
def delete_movie(id: int): 
    for item in movies:
    	if item["id"] == id:
            movies.remove(item)
            return movies







