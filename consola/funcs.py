import os
import sys
import json
from constantes import *


def jugar():
    niveles = ["facil", "intermedio", "dificil"]
    nivel_actual = 0
    puntos = 0

    while nivel_actual < len(niveles):
        nivel_actual, puntos = jugar_nivel(i_nivel=nivel_actual, nivel=niveles[nivel_actual], puntos=puntos)

    print("¡🎉 Felicitaciones, ganaste el juego!")

    en_mejores_10 = cargar_estadisticas(puntos=puntos)
    leer_estadisticas(print_stats=True)
    if en_mejores_10:
        print("🎖️ Ingresaste al ranking de los mejores 10")

def mostrar_juego(nivel: str, completadas: list[int], puntos: int = 0) -> None:
    datos_nivel = cargar_nivel(nivel)
    palabras = datos_nivel["palabras"]
    
    print(f"""{"-" * 20}
{" " * 5 + "CODY CROSS" + " " * 5}
{"-" * 20}
Puntos: {puntos}
{"-" * 20}
""")
    for i, palabra in enumerate(palabras):
        linea = f"{i + 1}. {palabra}" if i in completadas else f"{i + 1}. {"-" * len(palabra)}"
        print(linea)

def cargar_nivel(nivel: str, arch_niveles: str = ARCH_NIVELES) -> dict:
    with open(arch_niveles, "r", encoding="utf-8") as archivo_niveles:
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
            limpiar_terminal()
            print("¡✅ La palabra es correcta!")
            puntos += 10
            completadas.append(i_palabra - 1)
        else:
            limpiar_terminal()
            puntos -= 5
            print("❌ Esa no es la palabra, intentá de nuevo")
    
    mostrar_juego(nivel, completadas, puntos)
    print(f"¡🥳 Felicitaciones, ganaste el nivel {nivel}!")
    return i_nivel + 1, puntos

def creditos():
    """
    Muestra un mensaje de créditos
    """
    print(MENSAJE_DE_CREDITOS)

def cargar_estadisticas(puntos: int, arch_estad: str = ARCH_ESTAD) -> bool:
    """
    Carga el nombre y los puntos del jugador en un archivo .txt
    """

    nombre_completo = input("Ingresá tu nombre completo: ")[:12].strip()

    estadisticas: list[str] = leer_estadisticas(print_stats=False)
    puntajes = [int(linea.split(" - ")[1]) for linea in estadisticas]

    if not puntajes or len(puntajes) < 10 or (len(puntajes) == 10 and puntos > puntajes[-1]):
        estadisticas.append(f"{nombre_completo} - {puntos}")
        estadisticas.sort(key=lambda x: int(x.split(" - ")[1]), reverse=True)

        with open(arch_estad, "w") as file:
            file.writelines([f"{linea}\n" for linea in estadisticas][:10])
        
        return True
    else:
        return False

def leer_estadisticas(arch_estad: str = ARCH_ESTAD, print_stats: bool = True) -> list[str]:
    with open(arch_estad, "r") as file:
        lineas = file.readlines()

    estadisticas = [linea.replace("\n", "") for linea in lineas]
    
    if print_stats:
        print(MENSAJE_DE_ESTADISTICAS)
        for i, jugador in enumerate(estadisticas):
            nombre, puntos = jugador.split(" - ")
            if i == 0:
                print(f"🥇 - {nombre}: {puntos}")
            elif i == 1:
                print(f"🥈 - {nombre}: {puntos}")
            elif i == 2:
                print(f"🥉 - {nombre}: {puntos}")
            else:
                print(f" {i + 1} - {nombre}: {puntos}")

    return estadisticas

def salir():
    """
    Termina el programa de forma armoniosa
    """
    print(MENSAJE_DE_SALIDA)
    sys.exit(0)

def menu(error: bool = False) -> int:
    """
    Muestra el menú en la terminal y devuelve la opción elegida por el usuario
    """
    limpiar_terminal()
    print(MENU)

    if error:
        print("❌ Error: ingresá un número del 1 al 4.")

    eleccion = input("Ingresá la opción correspondiente y apretá Enter: ")
    if not eleccion.isdigit():
        return menu(error=True)

    eleccion = int(eleccion)
    if eleccion not in range(1, 5):
        return menu(error=True)
    
    limpiar_terminal()
    return eleccion

def limpiar_terminal() -> None:
    """
    Limpia la terminal tanto para sistemas operativos Windows como para sistemas operativos macOS y Linux
    """
    os.system("cls" if os.name == "nt" else "clear")
        
