# crear un entorno virtual 
python3 -m venv env 

# activar entorno virtual
source env/bin/activate

# en caso se necesite actualizar pip3
python3 -m pip3 install --upgrade pip3

# instalar fastapi 
pip3 install fastapi 

# modulo para ejecutar fastapi
pip3 install uvicorn

# correr el servicio 
uvicorn main:app --reload

# correr el servicio con un puerto especifico
uvicorn main:app --reload --port 5000

# correr el servicio con un puerto especifico y 
# que puede accederse desde cualquier host 
uvicorn main:app --reload --port 5000 --host 0.0.0.0


# algunos articulos de interes 
https://www.linkedin.com/pulse/fastapi-vs-django-flask-germ%C3%A1n-salina-ccmgf/?trackingId=xFO%20D1im3HDFakdN1WHong




