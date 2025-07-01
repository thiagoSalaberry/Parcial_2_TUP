import pygame
from interfaz_grafica.estado import get_estado, set_estado
from interfaz_grafica.eventos import on, trigger
from componentes.boton import *
from consola.funciones import leer_estadisticas, cargar_estadisticas
from constantes import ARCH_NIVELES
import json
import os


# def cargar_nombre(letra: str) -> None:
#     nombre_jugador = get_estado("nombre_jugador")



def ingresar_letra(letra: str, campo: str) -> None:
    """
    Carga la letra ingresada por el usuario en el campo del estado pertinente.
    Args:
        letra (str): Caracter ingresada por el usuario
        campo (str): Campo del estado a alterar
    Returns:
        None
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
    Returns:
        None
    """
    if campo == "palabra_actual":
        i_palabra_actual, palabras_completadas, palabra_actual = get_estado("i_palabra_actual"), get_estado("palabras_completadas"), get_estado("palabras_completadas")[i_palabra_actual][:-1]
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
    Args:
        None
    Returns:
        None
    """
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
    """
    Verifica que la palabra actual ingresada por el usuario se igual a la determinada por el juego. En tal caso, dispara el evento de 'palabra_completada'
    Args:
        None
    Returns:
        None
    """
    palabra_actual, palabras = get_estado("palabra_actual"), get_estado("palabras")
    if len(palabra_actual) == len(palabras[0]):
        trigger("palabra_completada")


def ganar_nivel() -> None:
    """
    Cambia el estado del nivel actual a ganado y reproduce un sonido
    Args:
        None
    Returns:
        None
    """
    set_estado({ "estado_nivel_actual": "ganado" })
    sound("ganar")


def ganar_juego() -> None:
    """
    Cambia el estado del juego a ganado y reproduce un sonido
    Args:
        None
    Returns:
        None
    """
    set_estado({ "juego_ganado": True })
    sound("ganar")


def siguiente_nivel() -> None:
    """
    Manejar el cambio de nivel, altera el estado y dispara el evento 'cambio_de_nivel'
    Args: 
        None
    Returns: 
        None
    """
    nivel_actual = get_estado("nivel_actual")
    siguiente = "intermedio" if nivel_actual == "facil" else "dificil"
    set_estado({ "nivel_actual": siguiente })
    trigger("cambio_de_nivel")


def cambiar_nivel() -> None:
    """
    Altera el estado avanzando y reiniciando el estado del nivel siguiente
    Args:
        None
    Returns:
        None
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


def nivel_terminado():
    """
    Evalúa que todas las palabras ingresadas por el usuario sean correctas. En tal caso, dispara el evento 'nivel_ganado'
    Args:
        None
    Returns: 
        None
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
    Args:
        None
    Returns:
        None
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
    Args:
        None
    Returns:
        None
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
    Returns:
        None
    """
    if pantalla not in ["inicio", "jugar", "estadisticas", "creditos"]:
        raise ValueError("'pantalla' debe ser 'inicio', 'jugar', 'estadisticas' o 'creditos'.")

    set_estado({"pantalla": pantalla})


def volver() -> None:
    """
    Vuelve a la pantall de inicio y reinicia el estado.
    Args:
        None
    Returns:
        None
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


def leer_niveles(arch_niveles: str = ARCH_NIVELES) -> dict:
    """
    Lee el archivo de los datos de los niveles.
    Args:
        arch_niveles (str): Nombre del archivo
    Returns:
        None
    """
    with open(arch_niveles, "r", encoding="utf-8") as archivo_niveles:
        datos_niveles = json.load(archivo_niveles)
    
    return datos_niveles["niveles"]


def sound(audio: str) -> None:
    """
    Reproduce un sonido.
    Args:
        audio (str): Nombre del archivo de audio a reproducir
    Returns:
        None
    """
    archivo = os.path.join("assets", f"{audio}.mp3")
    sound = pygame.mixer.Sound(archivo)
    sound.play()


def grupo(
    elementos: list[dict],
    direccion: str = "horizontal",
    gap: int = 10,
    pos_inicial: tuple[int, int] = (0, 0),
    area: pygame.Surface = None,
    eventos: list[pygame.event.Event] = None
) -> None:
    """
    Esta es una función que simula el comportamiento de un div con display flex en HTML. Recibe una lista de elementos y los renderiza de manera continua separados por un gap.
    Args:
        elementos (list[dict]): Elementos a renderizar
        dirección (str): Horizontal o vertical
        gap (int): Separación entre elementos
        pos_inicial (tuple[int, int]): Posición a partir de la cual se renderizarán los elementos
        area (pygame.Surface): Superficie sobre la cual se renderizarán los elementos
        eventos (list[pygame.event.Event]): Lista de eventos pasados a los elementos que los necesiten
    Returns:
        None
    """
    x_actual, y_actual = pos_inicial

    for el in elementos:
        ancho = el.get("ancho")
        alto = el.get("alto")

        if "render" in el:
            # render es un método estándar de cada uno de los distintos tipos de elementos que se encarga de renderizar y manejar los eventos del elemento
            el["render"](area, (x_actual, y_actual), eventos)
        
        if direccion == "horizontal":
            x_actual += ancho + gap
        elif direccion == "vertical":
            y_actual += alto + gap

def wrap_boton(boton_dict: dict, font: pygame.font.Font) -> None:
    """
    Esta es una función que se encarga de estandarizar los elementos 'boton'. Los crea y define cómo renderizarlos. Devuelve un objeto listo para ser usado por la frunción 'grupo'
    Args:
        boton_dict (dict): Datos del botón (Texto y función a ejecutar al hacer click)
    Returns:
        render (callable): Forma de renderizar el botón
        ancho (int): Ancho del botón
        alto (int): Alto del botón
    """
    data_boton = crear_boton(0, 0, boton_dict["valor"], boton_dict["callback"], font=font)

    def render(area: pygame.Surface, pos: tuple[int, int], eventos: list[pygame.event.Event]) -> None:
        data_boton["rect"].topleft = pos
        data_boton["sombra_rect"].topleft = (pos[0], pos[1] + 4)
        pygame.draw.rect(area, COLOR_BOTON_SOMBRA, data_boton["sombra_rect"], border_radius=5)
        pygame.draw.rect(area, COLOR_BOTON, data_boton["rect"], border_radius=5)
        area.blit(
            data_boton["area_texto"],
            (
                data_boton["rect"].centerx - data_boton["area_texto"].get_width() // 2,
                data_boton["rect"].centery - data_boton["area_texto"].get_height() // 2,
            )
        )
        manejar_click_boton(data_boton, eventos)
    
    return {
        "render": render,
        "ancho": data_boton["ancho"],
        "alto": data_boton["alto"],
    }