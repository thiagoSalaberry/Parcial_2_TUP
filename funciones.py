import os
import sys
import json

def jugar():
    mostrar_juego("facil")

def mostrar_juego(nivel: str, completadas: list[int], puntos: int = 0) -> None:
    datos_nivel = cargar_nivel(nivel)
    palabras = datos_nivel["palabras"]
    
    print("-" * 20)
    print(" " * 5 + "CODY CROSS" + " " * 5)
    print("-" * 20)
    print(f"Puntos: {puntos}")
    print("-" * 20)
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

def jugar_nivel(i_nivel: int, nivel: str, puntos: int = 0) -> int:
    completadas = []
    while len(completadas) < 8:
        datos_nivel = cargar_nivel(nivel)
        palabras = datos_nivel["palabras"]
        pistas = datos_nivel["pistas"]
        mostrar_juego(nivel, completadas, puntos)
        
        while True:
            i_palabra = input("Ingresá la palabra a cargar: ")
            if not i_palabra.isdigit():
                print("❌ Error: ingresá un número del 1 al 8")
                continue
            i_palabra = int(i_palabra)
            if i_palabra not in range(1, 9):
                print("❌ Error: ingresá un número del 1 al 8")
                continue
            if i_palabra - 1 in completadas:
                print(f"⚠️  La palabra {i_palabra} ya está completada, elegí otra")
                continue
            break
        
        print(f"Pista para la palabra {i_palabra}: {pistas[i_palabra - 1]}")
        while True:
            palabra = input("Ingresá la palabra: ")
            if len(palabra) != len(palabras[0]):
                print(f"❌ Error: ingresá una palabra de {len(palabras[0])} letras")
                continue
            break
        
        if palabra.strip().upper() == palabras[i_palabra - 1]:
            os.system("cls")
            print("¡✅ La palabra es correcta!")
            puntos += 10
            completadas.append(i_palabra - 1)
        else:
            os.system("cls")
            puntos -= 5
            print("❌ Esa no es la palabra, intentá de nuevo")
    
    mostrar_juego(nivel, completadas, puntos)
    print(f"¡🥳 Felicitaciones, ganaste el nivel {nivel}!")
    return i_nivel + 1, puntos

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

def cargar_estadisticas(puntos: int) -> None:
    """
    Carga el nombre y los puntos del jugador en un archivo .txt
    """
    nombre_completo = input("Ingresá tu nombre completo: ")
    print(f"{nombre_completo}: {puntos}")
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