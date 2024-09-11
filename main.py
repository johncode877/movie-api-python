from fastapi import FastAPI
from fastapi.responses import HTMLResponse


from config.database import engine,Base
from middleware.error_handler import ErrorHandler
from routers.movie import movie_router 
from routers.user import user_router 


# instancia de fastapi
app = FastAPI()

app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

# se añade a la aplicacion un middleware de manejo de errores


app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)


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








