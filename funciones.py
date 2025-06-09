import os
import sys
import json

def jugar():
    mostrar_juego("facil")

def mostrar_juego(nivel: str, completadas: list[int] = None) -> None:
    datos_nivel = cargar_nivel(nivel)
    palabras = datos_nivel["palabras"]
#     print(f"""{"-"*20}
# {" "*5}CODY CROSS
# {"-"*20}
# Puntaje: 0
# {"-"*20}
# {"\n".join([f"{i + 1}. {palabra}" for i, palabra in enumerate(palabras) if i in completadas])}
# """)
    for i, palabra in enumerate(palabras):
        linea = f"{i + 1}. {palabra}" if i in completadas else f"{i + 1}. {"-" * len(palabra)}"
        print(linea)

def cargar_nivel(nivel: str) -> dict:
    ruta_niveles = "."
    nombre_niveles = "niveles.json"
    with open(os.path.join(ruta_niveles, nombre_niveles), "r", encoding="utf-8") as archivo_niveles:
        datos_niveles = json.load(archivo_niveles)
        datos_nivel = datos_niveles["niveles"][nivel]
    
    return datos_nivel


def creditos():
    msj_creditos = """Créditos

***DESCRIPCIÓN***
Autores: Bautista Ruiz y Thiago Salaberry
Fecha de desarrollo: Junio a Julio de 2025
Detalles de la materia: Programación I
Docente: Prof. Martín Alejandro García y Verónica Natalia Carbonari
Carrera: Tecnicatura Universitaria en Programación - UTN Avellaneda
Mails de contacto: bautyruiz1011@gmail.com y thiagosalaberry99@gmail.com
"""
    print(msj_creditos)

def cargar_estadisticas(nombre_completo: str, puntos: int) -> None:
    """
    Carga el nombre y los puntos del jugador en un archivo .txt
    """
    estadisticas = leer_estadisticas()

    pass

def leer_estadisticas():
    """
    Lee un archivo .txt
    """
    pass

def salir():
    print("👋 Hasta la próxima!")
    sys.exit(0)