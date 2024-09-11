# crear un entorno virtual 
python3 -m venv env 

# activar entorno virtual
source env/bin/activate

# en caso se necesite actualizar pip3
python3 -m pip3 install --upgrade pip3

# instalar todas las dependencias 
pip3 install -r requirements.txt

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

# Instalar del plugin SQLite viewer en Visual Studio Code 

# instalar modulo para manejar el token
pip3 install pyjwt 

# instalar modulo sqlalchemy para manejar base de datos 
pip3 install sqlalchemy 



# Contenerizar la aplicacion 
 Vamos a seguir la guia definida en 
https://docs.docker.com/guides/language/python/containerize/


# Montar base de datos 
https://docs.docker.com/engine/storage/bind-mounts/

El archivo database.sql de base de datos se coloco dentro 
de una carpeta db
En el archivo Dockerfile, se hizo un mount de tipo bind 
al archivo que estaba en el repositorio del fuente 
Sobre el sistema operativo host, se actualizaron los permisos
recursivamente al directorio db , para evitar
los errores "OperationalError: attempt to write a readonly database"
cuando se ejecutaba el contenedor
Estando en el directorio del proyectos se ejecuto el siguiente comando

chmod -R o+w db 


# Correr la aplicacion 
Estando dentro del directorio del proyecto 
ejecutar el siguiente comando, para correr 
la aplicacion

docker compose up --build

o para correr la aplicacion en background 
ejecutar el siguiente comando 

docker compose up --build -d

para detener la aplicacion    
ejecutar el siguiente comando 

docker compose down 



# Trabajando con postgresql

Debemos crear una base de datos postgresql (movie)
luego ejecutar los scripts de la carpeta

db/1_create.sql 
db/2_grants.sql 

Instalar el paquete python-dotenv

pip3 install python-dotenv

Crear las siguientes variable de entorno 
en tu host 

Estas variables serviran para conectar
a tu base de datos postgresql desde 
el contenedor de tu aplicacion 

export DB_USER     = xxxxxx
export DB_PASSWORD = yyyyyy
export DB_NAME     = zzzzzz

puedes registrarlas en el archivo
/etc/profile y luego las recargas con el siguiente 
comando 
source /etc/profile

# Instalar el paquete de dependencia 
# para postgresql

pip3 install psycopg2-binary


# Usando compose watch

Despues de añadir la configuracion 
compose watch en el archvio compose.yaml 

ejecutamos a la aplicacion usando 

docker compose watch

luego cualquier cambio en la aplicacion 
se vera inmediatamente reflejado en el 
contenedor en ejecucion 


# Algunos articulos de interes 

https://www.linkedin.com/pulse/fastapi-vs-django-flask-germ%C3%A1n-salina-ccmgf/?trackingId=xFO%20D1im3HDFakdN1WHong

https://bitybyte.github.io/Organzando-codigo-Python/

https://fastapi.tiangolo.com/tutorial/bigger-applications/

https://devtodevops.com/keep-docker-container-running/

https://www.baeldung.com/ops/running-docker-containers-indefinitely

https://docs.docker.com/guides/language/python/develop/

