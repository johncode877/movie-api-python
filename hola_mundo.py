#hola_mundo.py
import os

def hola_mundo():
  nombre = os.getenv("USERNAME")	
  print(f"!Hola , {nombre} desde GitHub!")

if __name__ == '__main__':
  hola_mundo()
