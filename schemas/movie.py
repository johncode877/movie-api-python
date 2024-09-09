from typing import Optional
from pydantic import BaseModel, Field



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

    