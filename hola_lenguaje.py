#hola_lenguaje.py
import os

def hola_lenguaje():
  nombre = os.getenv("USERNAME")
  language = os.getenv("LANGUAGE")  
  print(f"!Hola , {nombre} mi lenguaje favorito es {language} !")

if __name__ == '__main__':
  hola_lenguaje()
