#hola_lenguaje.py
import os

def hola_lenguaje():
  nombre = os.getenv("USERNAME")	
  print(f"!Hola , {nombre} desde GitHub!")

if __name__ == '__main__':
  hola_lenguaje()
