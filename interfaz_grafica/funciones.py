import sys
import os
import pygame
from pygame import Surface
from pygame.font import Font
from estado import get_estado, set_estado
from constantes import pant_creditos, pant_estadisticas
from utils import leer_niveles
data_niveles = leer_niveles()


def render_el(area: Surface, eventos: list[pygame.event.Event], el: dict, font: Font) -> None:
    """
    Renderiza un elemento según su tipo.
    Args:
        area (Surface): Superfici de pygame sobre la cual renderizar los elementos
        eventos (list[pygame.event.Event]): Lista de eventos a pasar a cada uno de los elementos que los necesiten
        el (dict): Elemento a renderizar
        font (Font): Fuente con la que renderizar los textos
    """
    match el["tipo"]:
        case "texto":
            texto(area, el, font)
        case "boton":
            button(area, el, eventos, font)
        case "palabra":
            palabra(area, eventos, el)
        case "*":
            raise("⚠️  El elemento a renderizar es de un tipo no soportado")
            


def render_pantalla(
    area: Surface,
    eventos: list[pygame.event.Event],
    font: pygame.font.Font = None
) -> None:
    """
    - Lee el estado y obtiene la pantalla actual.
    - Obtiene los elementos a renderizar según la pantalla
    - Llama a render_el y le pasa cada uno de los elementos
    Recibe el area sobre la cual renderizar y los eventos a pasar
    """
    pantalla = get_estado("pantalla")
    nivel_actual, juego_ganado = get_estado("nivel_actual"), get_estado("juego_ganado")
    volver_dict = {"tipo": "boton", "valor": "Volver", "callback": volver, "pos": (15, 535)}
    # INICIO 👇
    if pantalla == "inicio":
        botones_dict = [
            {"valor": "Jugar", "callback": lambda: set_estado({"pantalla": "jugar"})},
            {"valor": "Estadisticas", "callback": lambda: set_estado({"pantalla": "estadisticas"})},
            {"valor": "Créditos", "callback": lambda: set_estado({"pantalla": "creditos"})},
            {"valor": "Salir", "callback": lambda: sys.exit(0)},
        ]
        botones = []
        for i, boton_dict in enumerate(botones_dict):
            boton = wrap_boton(
                boton_dict,
                font
            )
            botones.append(boton)
        grupo(
            botones,
            "horizontal",
            10,
            ((800 - sum(b["ancho"] for b in botones) - 10 * (len(botones) - 1)) / 2, 600 - 75),
            area,
            eventos
        )
    
    # JUGAR 👇
    elif pantalla == "jugar":
        palabras, palabras_completadas, pistas, i_palabra_actual, estado_nivel_actual, nivel_actual, score = get_estado("palabras"), get_estado("palabras_completadas"), get_estado("pistas"), get_estado("i_palabra_actual"), get_estado("estado_nivel_actual"), get_estado("nivel_actual"), get_estado("score")
        for i, correcta in enumerate(palabras):
            ingresada = palabras_completadas[i]
            palabra = wrap_palabra(
                correcta,
                ingresada,
                i,
                i_palabra_actual,
                lambda: set_estado({"i_palabra_actual": i}),
                font
            )
            x = (800 - palabra["ancho"]) // 2
            y = 70 + 54 * i
            palabra["render"](area, (x, y), eventos)
        niveles_map = {
            "facil": "1",
            "intermedio": "2",
            "dificil": "3",
        }
        nivel = {"tipo": "texto", "valor": f"Nivel: {niveles_map[nivel_actual]}", "pos": (665, 30)}
        score = {"tipo": "texto", "valor": f"Puntos: {score}", "pos": (680, 50)}
        pista = {"tipo": "texto", "valor": f"{pistas[i_palabra_actual]}", "pos": (400, 510)}
        render_el(area, eventos, nivel, font)
        render_el(area, eventos, score, font)
        render_el(area, eventos, pista, font)

        if estado_nivel_actual == "ganado" and nivel_actual != "dificil":
            siguiente_dict = { "tipo": "boton", "valor": "Siguiente nivel", "callback": siguiente_nivel, "pos": (585, 535) }
            button(area, siguiente_dict, eventos, font)

        if not juego_ganado:
            render_el(area, eventos, volver_dict, font)
        else:
            elementos = [
                wrap_texto({"valor": "¡FELICITACIONES!"}, font),
                wrap_texto({"valor": f"Ganaste el juego con {get_estado("score")} puntos"}, font),
                wrap_texto({"valor": "Ingresá tu nombre:"}, font),
                wrap_input({"valor": get_estado("nombre_jugador")}, font),
                wrap_boton({"valor": "Cargar puntos", "callback": lambda: trigger("nombre_cargado")}, font)
            ]

            recuadro = wrap_recuadro(elementos, padding=(40, 20), gap=20, direccion="vertical", font=font)

            # Centramos el recuadro en pantalla
            x = (800 - recuadro["ancho"]) // 2
            y = (600 - recuadro["alto"]) // 2
            recuadro["render"](area, (x, y), eventos)

    # ESTADÍSTICAS 👇
    elif pantalla == "estadisticas":
        estadisticas = leer_estadisticas(print=False)
        wrappeables = []
        render_el(area, eventos, pant_estadisticas[0], font)
        for el in pant_estadisticas[1:]:
            if el["tipo"] == "texto":
                wrappeables.append(wrap_texto({"valor": el["valor"]}, font))
        for i, jugador in enumerate(estadisticas):
            wrappeables.append(wrap_texto({"valor": f"{i + 1}. {jugador}"}, font))
        recuadro = wrap_recuadro(wrappeables, padding=(40, 20), gap=10, direccion="vertical", jusfify="left", font=font)
        # Centramos el recuadro en pantalla
        x = (800 - recuadro["ancho"]) // 2
        y = (600 - recuadro["alto"]) // 2
        recuadro["render"](area, (x, y), eventos)
        render_el(area, eventos, volver_dict, font)
    
    # CRÉDITOS 👇
    elif pantalla == "creditos":
        wrappeables = []
        render_el(area, eventos, pant_creditos[0], font)
        for el in pant_creditos[1:]:
            wrappeables.append(wrap_texto({"valor": el["valor"]}, font))
        recuadro = wrap_recuadro(wrappeables, padding=(20, 10), gap=0, direccion="vertical", jusfify="left", font=font)
        # Centramos el recuadro en pantalla
        x = (800 - recuadro["ancho"]) // 2
        y = (600 - recuadro["alto"]) // 2
        recuadro["render"](area, (x, y), eventos)
        render_el(area, eventos, volver_dict, font)



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

def wrap_boton(boton_dict: dict, font: pygame.font.Font) -> dict:
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