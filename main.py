from fastapi import FastAPI
from config.database import engine,Base
from middleware.error_handler import ErrorHandler
from routers.movie import movie_router 
from routers.user import user_router 


# instancia de fastapi
app = FastAPI()

app.title = "CRUD Movie API"
app.version = "0.0.1"

# se añade a la aplicacion un middleware de manejo de errores

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)






