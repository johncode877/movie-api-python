from fastapi import APIRouter
from fastapi import Depends,Path,Query,status
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from typing import List, Optional
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middleware.jwt_bearer import JWTBearer

from services.movie import MovieService


movie_router = APIRouter()

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
    


@movie_router.get('/movies',tags=['movies'],response_model=List[Movie],status_code=200,dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
  db = Session()
  result = MovieService(db).get_movies()
  
  return JSONResponse(status_code=200,content=jsonable_encoder(result))

# id es un parameter path
@movie_router.get('/movies/{id}',tags=['movies'],response_model=Movie)
def get_movie(id:int=Path(ge=1,le=2000)) -> Movie:

   db = Session()
   result = MovieService(db).get_movie(id)
   
   if not result:
     return JSONResponse(status_code=404,content={'message':"No encontrado"}) 
   
   return JSONResponse(status_code=200,content=jsonable_encoder(result))
    

# category es un parameter query
@movie_router.get('/movies/',tags=['movies'],response_model=List[Movie],status_code=200)
def get_movies_by_category(category:str=Query(min_length=5,max_length=15)) -> List[Movie]:
   
   db = Session()   
   result = MovieService(db).get_movies_by_category(category)
   return JSONResponse(status_code=200,content=jsonable_encoder(result)) 

# para que los campos se han considerados
# como parte del request body y no como variable query 
# es necesario asignarles que son de tipo Body	       
@movie_router.post('/movies',tags=['movies'], response_model=dict,status_code=201)
def create_movie(movie:Movie) -> dict:

    db = Session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    # convierte el objeto Movie (pydantic) a un diccionario
    # para que pueda ser añadido a la lista de diccionarios
    # de movies 
    
    return JSONResponse(status_code=201,content={"message":"Se ha registrado la pelicula"})


@movie_router.put('/movies/{id}',tags=['movies'],response_model=dict,status_code=200)
def update_movie(id: int, movie: Movie) -> dict:

    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id==id).first()
    if not result:
     return JSONResponse(status_code=404,content={'message':"No encontrado"}) 
    
    result.title = movie.title
    result.category = movie.category
    result.rating = movie.rating
    result.overview = movie.overview
    result.year = movie.year

    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK,content={"message":"Se ha modificado la pelicula"})

# response_model indica el modelo de respuesta
@movie_router.delete('/movies/{id}',tags=['movies'],response_model=dict,status_code=200)
def delete_movie(id: int) -> dict: 

    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id==id).first()
    if not result:
     return JSONResponse(status_code=404,content={'message':"No encontrado"}) 

    db.delete(result)
    db.commit()    
    return JSONResponse(status_code=200,content={"message":"Se ha eliminado la pelicula"})
