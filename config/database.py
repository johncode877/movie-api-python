import os 
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

# permite manipular las tablas de mi base de datos
from sqlalchemy.ext.declarative import declarative_base


# cuando se usa sqlite 
#sqlite_file_name = "../db/database.sqlite"
#base_dir = os.path.dirname(os.path.realpath(__file__))
#database_url = f"sqlite:///{os.path.join(base_dir,sqlite_file_name)}"

import os
from dotenv import load_dotenv

load_dotenv()

DB_USER=os.getenv("DB_USER") 
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_NAME=os.getenv("DB_NAME")


database_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}" 

engine = create_engine(database_url,echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()

