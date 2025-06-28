import pygame
from estado import get_estado, set_estado
from eventos import on, trigger
from constantes import ARCH_NIVELES
import json
import os

def ingresar_letra(letra: str) -> None:
    i_palabra_actual = get_estado("i_palabra_actual")
    palabras_completadas = get_estado("palabras_completadas")
    nivel_actual = get_estado("nivel_actual")

    if nivel_actual == "facil":
        largo_palabras = 4
    elif nivel_actual == "intermedio":
        largo_palabras = 8
    elif nivel_actual == "dificil":
        largo_palabras = 10
    palabra_actual = palabras_completadas[i_palabra_actual]

    if len(palabra_actual) < largo_palabras:
        palabra_actual += letra
        palabras_completadas[i_palabra_actual] = palabra_actual
        set_estado({
            "palabras_completadas": palabras_completadas,
            "palabra_actual": palabra_actual
        })
        verificar_palabra()
        nivel_terminado()
        juego_terminado()


def borrar_letra() -> None:
    i_palabra_actual = get_estado("i_palabra_actual")
    palabras_completadas = get_estado("palabras_completadas")
    palabra_actual = get_estado("palabras_completadas")[i_palabra_actual][:-1]
    palabras_completadas[i_palabra_actual] = palabra_actual
    set_estado({
        "palabras_completadas": palabras_completadas,
        "palabra_actual": palabra_actual,
    })


def siguiente() -> None:
    acertadas, i_palabra_actual = get_estado("acertadas"), get_estado("i_palabra_actual")
    total = len(acertadas)

    # Buscar hacia adelante
    for i in range(i_palabra_actual + 1, total):
        if not acertadas[i]:
            set_estado({ "i_palabra_actual": i })
            return

    # Buscar desde el principio hasta la actual
    for i in range(0, i_palabra_actual):
        if not acertadas[i]:
            set_estado({ "i_palabra_actual": i })
            return

    # Todas acertadas
    return None


def verificar_palabra():
    palabra_actual, palabras = get_estado("palabra_actual"), get_estado("palabras")
    if len(palabra_actual) == len(palabras[0]):
        trigger("palabra_completada")


def handle_win_level() -> None:
    set_estado({ "estado_nivel_actual": "ganado" })
    sound("ganar")


def handle_win_game() -> None:
    print("¡🎉 FELICIDADES, GANASTE EL JUEGO!")
    set_estado({ "juego_ganado": True })
    sound("ganar")


def siguiente_nivel() -> None:
    nivel_actual = get_estado("nivel_actual")
    siguiente = "intermedio" if nivel_actual == "facil" else "dificil"
    set_estado({ "nivel_actual": siguiente })
    trigger("cambio_de_nivel")


def handle_level_change() -> None:
    data_niveles = leer_niveles()
    nivel_actual = get_estado("nivel_actual")
    nuevo_estado = {
        "estado_nivel_actual": "jugando",
        "i_palabra_actual": 0,
        "palabra_actual": "",
        "palabras_completadas": [""] * 8,
        "palabras": data_niveles[nivel_actual]["palabras"],
        "acertadas": [False] * 8,
        "palabras_validadas": [False] * 8,
        "pistas": data_niveles[nivel_actual]["pistas"],
    }
    set_estado(nuevo_estado)


def nivel_terminado():
    acertadas = get_estado("acertadas")
    ganado = True
    for acertada in acertadas:
        if not acertada:
            ganado = False
    if ganado:
        trigger("nivel_ganado")


def juego_terminado() -> None:
    nivel_actual, acertadas = get_estado("nivel_actual"), get_estado("acertadas")
    juego_ganado = True
    for acertada in acertadas:
        if not acertada:
            juego_ganado = False
    if nivel_actual == "dificil" and juego_ganado:
        trigger("juego_ganado")



def handle_points() -> None:
        i_palabra_actual = get_estado("i_palabra_actual")
        palabra_correcta = get_estado("palabras")[i_palabra_actual]
        palabras = get_estado("palabras")
        palabra_actual = get_estado("palabra_actual")
        acertadas = get_estado("acertadas")
        score = get_estado("score")
        if len(palabra_actual) == len(palabras[0]):
            if palabra_actual == palabra_correcta:
                acertadas[i_palabra_actual] = True
                sound("correcto")
                set_estado({ "score": score + 10, "acertadas": acertadas })
                siguiente()
            else:
                sound("error")
                set_estado({ "score": score - 5 })


def cambiar_pantalla(pantalla: str) -> None:
    if pantalla not in ["inicio", "jugar", "estadisticas", "creditos"]:
        raise ValueError("'pantalla' debe ser 'inicio', 'jugar', 'estadisticas' o 'creditos'.")

    set_estado({"pantalla": pantalla})


def leer_niveles(arch_niveles: str = ARCH_NIVELES) -> dict:
    with open(arch_niveles, "r", encoding="utf-8") as archivo_niveles:
        datos_niveles = json.load(archivo_niveles)
    
    return datos_niveles["niveles"]


def sound(audio: str) -> None:
    archivo = os.path.join("assets", f"{audio}.mp3")
    sound = pygame.mixer.Sound(archivo)
    sound.play()
