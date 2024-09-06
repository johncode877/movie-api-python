from fastapi import FastAPI,Body,Path,Query,status
from fastapi.responses import HTMLResponse,JSONResponse
from pydantic import BaseModel,Field
from typing import List, Optional
from jwt_manager import create_token

# instancia de fastapi
app = FastAPI()

app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"


class User(BaseModel):
    email:str
    password:str




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


@app.post('/login',tags=['auth'])
def login(user: User):

    if user.email == "admin@gmail.com" and user.password == "admin":
       token:str = create_token(user.model_dump())
    return JSONResponse(status_code=200,content=token)

@app.get('/movies',tags=['movies'],response_model=List[Movie],status_code=200)
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200,content=movies)

# id es un parameter path
@app.get('/movies/{id}',tags=['movies'],response_model=Movie,status_code=200)
def get_movie(id:int=Path(ge=1,le=2000)) -> Movie:
    for item in movies:
        if item["id"] == id:
            return JSONResponse(status_code=200,content=item)
    
    return JSONResponse(status_code=404,content=[])

# category es un parameter query
@app.get('/movies/',tags=['movies'],response_model=List[Movie],status_code=200)
def get_movies_by_category(category:str=Query(min_length=5,max_length=15)) -> List[Movie]:
   data = [item for item in movies if item["category"] == category]
   if(data):
     return JSONResponse(status_code=200,content=data)
   else:
     return JSONResponse(status_code=404,content=data)      
   
   return JSONResponse(content=data)

# para que los campos se han considerados
# como parte del request body y no como variable query 
# es necesario asignarles que son de tipo Body	       
@app.post('/movies',tags=['movies'], response_model=dict,status_code=201)
def create_movie(movie:Movie) -> dict:
    # convierte el objeto Movie (pydantic) a un diccionario
    # para que pueda ser añadido a la lista de diccionarios
    # de movies 
    movies.append(movie.model_dump())
    return JSONResponse(status_code=201,content={"message":"Se ha registrado la pelicula"})


@app.put('/movies/{id}',tags=['movies'],response_model=dict,status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title   
            item["overview"] = movie.overview
            item["year"] = movie.year   
            item["rating"] = movie.rating   
            item["year"] = movie.year   
            item["category"] = movie.category

    return JSONResponse(status_code=status.HTTP_200_OK,content={"message":"Se ha modificado la pelicula"})

# response_model indica el modelo de respuesta
@app.delete('/movies/{id}',tags=['movies'],response_model=dict,status_code=200)
def delete_movie(id: int) -> dict: 
    for item in movies:
    	if item["id"] == id:
            movies.remove(item)
    return JSONResponse(status_code=200,content={"message":"Se ha eliminado la pelicula"})







