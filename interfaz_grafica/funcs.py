"""
Este módulo se encarga de manejar toda la lógica relativa al juego
"""
import os
import pygame
from estado import get_estado, set_estado
from utils import leer_niveles
from eventos import trigger
from constantes import ASSETS_PATH


data_niveles = leer_niveles()


def ingresar_letra(letra: str, campo: str) -> None:
    """
    Carga la letra ingresada por el usuario en el campo del estado pertinente.
    Args:
        letra (str): Caracter ingresada por el usuario
        campo (str): Campo del estado a alterar
    """

    if campo == "palabra_actual":
        i_palabra_actual, palabras_completadas, nivel_actual = get_estado("i_palabra_actual"), get_estado("palabras_completadas"), get_estado("nivel_actual")
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
            # Disparamos todos los eventos pertinentes
            verificar_palabra()
            nivel_terminado()
            juego_terminado()

    elif campo == "nombre_jugador":
        max_largo_nombre = 12
        nombre_jugador = get_estado("nombre_jugador")
        if len(nombre_jugador) < max_largo_nombre:
            nombre_jugador += letra
            set_estado({"nombre_jugador": nombre_jugador})


def borrar_letra(campo: str) -> None:
    """
    Borra la última letra en el campo del estado pertinente
    Args:
        campo (str): Campo del estado a alterar
    """
    if campo == "palabra_actual":
        i_palabra_actual, palabras_completadas, palabra_actual = get_estado("i_palabra_actual"), get_estado("palabras_completadas"), get_estado("palabras_completadas")
        palabra_actual = palabras_completadas[i_palabra_actual][:-1]
        palabras_completadas[i_palabra_actual] = palabra_actual
        set_estado({
            "palabras_completadas": palabras_completadas,
            "palabra_actual": palabra_actual,
        })
    elif campo == "nombre_jugador":
        nombre_jugador = get_estado("nombre_jugador")
        nombre_jugador = nombre_jugador[:-1]
        set_estado({"nombre_jugador": nombre_jugador})


def siguiente() -> None:
    """
    Pasa a la siguiente palabra disponible para cargar en la fase del juego. Evalúa si la siguiente palabra disponible está hacia adelante o hacia atrás y saltea las que hayan sido cargadas correctamente.
    """
    acertadas, i_palabra_actual = get_estado("acertadas"), get_estado("i_palabra_actual")
    total = len(acertadas)

    # Buscamos hacia adelante
    for i in range(i_palabra_actual + 1, total):
        if not acertadas[i]:
            set_estado({ "i_palabra_actual": i })
            return

    # Buscamos desde el principio hasta la actual
    for i in range(0, i_palabra_actual):
        if not acertadas[i]:
            set_estado({ "i_palabra_actual": i })
            return

    # Todas las palabras fueron acertadas
    return None


def cambiar_palabra(i: int) -> None:
    """
    Pasa a la palabra clickeada por el mouse en caso de que no haya sido completada.
    Args:
        i (int): Índice de la palabra
    """
    acertadas = get_estado("acertadas")
    if acertadas[i]:
        return
    set_estado({"i_palabra_actual": i})


def verificar_palabra():
    """
    Verifica que la palabra actual ingresada por el usuario se igual a la determinada por el juego. En tal caso, dispara el evento de 'palabra_completada'
    """
    palabra_actual, palabras = get_estado("palabra_actual"), get_estado("palabras")
    if len(palabra_actual) == len(palabras[0]):
        trigger("palabra_completada")


def ganar_nivel() -> None:
    """
    Cambia el estado del nivel actual a ganado y reproduce un sonido
    """
    set_estado({ "estado_nivel_actual": "ganado" })
    sound("ganar")


def ganar_juego() -> None:
    """
    Cambia el estado del juego a ganado y reproduce un sonido
    """
    set_estado({ "juego_ganado": True })
    sound("ganar")


def siguiente_nivel() -> None:
    """
    Manejar el cambio de nivel, altera el estado y dispara el evento 'cambio_de_nivel'
    """
    nivel_actual = get_estado("nivel_actual")
    siguiente = "intermedio" if nivel_actual == "facil" else "dificil"
    set_estado({ "nivel_actual": siguiente })
    trigger("cambio_de_nivel")


def cambiar_nivel() -> None:
    """
    Altera el estado avanzando y reiniciando el estado del nivel siguiente
    """
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


def nivel_terminado() -> None:
    """
    Evalúa que todas las palabras ingresadas por el usuario sean correctas. En tal caso, dispara el evento 'nivel_ganado'
    """
    acertadas = get_estado("acertadas")
    ganado = True
    for acertada in acertadas:
        if not acertada:
            ganado = False
    if ganado:
        trigger("nivel_ganado")


def juego_terminado() -> None:
    """
    Evalúa que todas las palabras del nivel difícil sean correctas. En tal caso, el juego habrá sido ganado y disparará el evento 'juego_ganado'
    """
    nivel_actual, acertadas = get_estado("nivel_actual"), get_estado("acertadas")
    juego_ganado = True
    for acertada in acertadas:
        if not acertada:
            juego_ganado = False
    if nivel_actual == "dificil" and juego_ganado:
        trigger("juego_ganado")



def manejar_puntos() -> None:
    """
    Maneja la lógica de los puntos y altera el estado. En caso de que la palabra sea correcta, suma los puntos en el estado, pasa a la siguiente palabra disponible. Caso contrario, resta los puntos en el estado. Reproduce un sonido en ambos casos.
    """
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
    """
    Cambia la pantalla a renderizar alterando el estado.
    Args:
        pantalla (str): Pantalla a renderizar
    """
    if pantalla not in ["inicio", "jugar", "estadisticas", "creditos"]:
        raise ValueError("'pantalla' debe ser 'inicio', 'jugar', 'estadisticas' o 'creditos'.")

    set_estado({"pantalla": pantalla})


def volver() -> None:
    """
    Vuelve a la pantall de inicio y reinicia el estado.
    """
    data_niveles = leer_niveles()
    estado_inical = {
        "pantalla": "inicio",
        "nivel_actual": "facil",
        "estado_nivel_actual": "jugando",
        "palabras": data_niveles["facil"]["palabras"],
        "palabras_validadas": [False] * 8,
        "palabras_completadas": [""] * 8,
        "acertadas": [False] * 8,
        "pistas": data_niveles["facil"]["pistas"],
        "score": 0,
        "i_palabra_actual": 0,
        "palabra_actual": "",
        "juego_ganado": False,
        "nombre_jugador": ""
    }
    set_estado(estado_inical)


def sound(audio: str) -> None:
    """
    Reproduce un sonido.
    Args:
        audio (str): Nombre del archivo de audio a reproducir
    """
    archivo = os.path.join(ASSETS_PATH, f"{audio}.mp3")
    sound = pygame.mixer.Sound(archivo)
    sound.play()