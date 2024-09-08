from fastapi import FastAPI,Depends,Body,Path,Query, Request,status
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.exceptions import HTTPException
from pydantic import BaseModel,Field
from typing import List, Optional
from jwt_manager import create_token,validate_token
from fastapi.security import HTTPBearer
from config.database import Session,engine,Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder


# instancia de fastapi
app = FastAPI()

app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)


class JWTBearer(HTTPBearer):
    async def __call__(self,request:Request):
       auth = await super().__call__(request)
       data = validate_token(auth.credentials)
       if data['email'] != 'admin@gmail.com':
           raise HTTPException (status_code=403,detail="Credenciales invalidas")



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

@app.get('/movies',tags=['movies'],response_model=List[Movie],status_code=200,dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
  db = Session()
  result = db.query(MovieModel).all() 
  return JSONResponse(status_code=200,content=jsonable_encoder(result))

# id es un parameter path
@app.get('/movies/{id}',tags=['movies'],response_model=Movie,status_code=200)
def get_movie(id:int=Path(ge=1,le=2000)) -> Movie:

   db = Session()
   result = db.query(MovieModel).filter(MovieModel.id==id).first()
   if not result:
     return JSONResponse(status_code=404,content={'message':"No encontrado"}) 
   return JSONResponse(status_code=200,content=jsonable_encoder(result))
    

# category es un parameter query
@app.get('/movies/',tags=['movies'],response_model=List[Movie],status_code=200)
def get_movies_by_category(category:str=Query(min_length=5,max_length=15)) -> List[Movie]:
   
   db = Session()
   result = db.query(MovieModel).filter(MovieModel.category==category).all()
   return JSONResponse(status_code=200,content=jsonable_encoder(result)) 

# para que los campos se han considerados
# como parte del request body y no como variable query 
# es necesario asignarles que son de tipo Body	       
@app.post('/movies',tags=['movies'], response_model=dict,status_code=201)
def create_movie(movie:Movie) -> dict:

    db = Session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    # convierte el objeto Movie (pydantic) a un diccionario
    # para que pueda ser añadido a la lista de diccionarios
    # de movies 
    movies.append(movie.model_dump())
    return JSONResponse(status_code=201,content={"message":"Se ha registrado la pelicula"})


@app.put('/movies/{id}',tags=['movies'],response_model=dict,status_code=200)
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
@app.delete('/movies/{id}',tags=['movies'],response_model=dict,status_code=200)
def delete_movie(id: int) -> dict: 

    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id==id).first()
    if not result:
     return JSONResponse(status_code=404,content={'message':"No encontrado"}) 

    db.delete(result)
    db.commit()    
    return JSONResponse(status_code=200,content={"message":"Se ha eliminado la pelicula"})







