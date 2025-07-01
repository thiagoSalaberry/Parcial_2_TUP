"""
Este módulo se encarga de renderizar los elementos en la pantalla en base a valores estáticos o a valores del estado
"""
import sys
import pygame
from pygame import Surface
from pygame.font import Font
from ui import boton as btn, wrap_boton, texto, wrap_texto, wrap_input, wrap_palabra, wrap_recuadro
from estado import get_estado, set_estado
from funcs import volver, siguiente_nivel, cambiar_palabra
from constantes import pant_creditos, pant_estadisticas, ANCHO, ALTO
from eventos import trigger
from utils import leer_estadisticas


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


def render_el(area: Surface, eventos: list[pygame.event.Event], el: dict, font: Font) -> None:
    """
    Renderiza un elemento según su tipo.
    Args:
        area (Surface): Superficie de pygame sobre la cual renderizar los elementos
        eventos (list[pygame.event.Event]): Lista de eventos a pasar a cada uno de los elementos que los necesiten
        el (dict): Elemento a renderizar
        font (Font): Fuente con la que renderizar los textos
    """
    match el["tipo"]:
        case "texto":
            texto(area, el, font)
        case "boton":
            btn(area, el, eventos, font)
        case "*":
            raise("⚠️  El elemento a renderizar es de un tipo no soportado")
            

def render_pantalla(
    area: Surface,
    eventos: list[pygame.event.Event],
    font: pygame.font.Font = None
) -> None:
    """
    Renderiza una pantalla según el valor actual del estado
    Args:
        area (Surface): Superficie de pygame sobre la cual renderizar los elementos
        eventos (list[pygame.event.Event]): Lista de eventos a pasar a cada uno de los elementos que los necesiten
        font (Font): Fuente con la que renderizar los textos
    """
    pantalla = get_estado("pantalla")
    nivel_actual, juego_ganado = get_estado("nivel_actual"), get_estado("juego_ganado")
    volver_dict = {"tipo": "boton", "valor": "Volver", "callback": volver, "pos": (15, 535)}
    
    # PANTALLA INICIO 👇
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
            ((ANCHO - sum(b["ancho"] for b in botones) - 10 * (len(botones) - 1)) / 2, ALTO - 75),
            area,
            eventos
        )
    
    # PANTALLA JUGAR 👇
    elif pantalla == "jugar":
        palabras, palabras_completadas, pistas, i_palabra_actual, estado_nivel_actual, nivel_actual, score = get_estado("palabras"), get_estado("palabras_completadas"), get_estado("pistas"), get_estado("i_palabra_actual"), get_estado("estado_nivel_actual"), get_estado("nivel_actual"), get_estado("score")
        for i, correcta in enumerate(palabras):
            ingresada = palabras_completadas[i]
            palabra = wrap_palabra(
                correcta,
                ingresada,
                i,
                i_palabra_actual,
                lambda: cambiar_palabra(i),
                font
            )
            x = (ANCHO - palabra["ancho"]) // 2
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
            # Si el nivel actual fue ganado, se renderiza el botón de 'Siguiente nivel'
            siguiente_dict = { "tipo": "boton", "valor": "Siguiente nivel", "callback": siguiente_nivel, "pos": (585, 535) }
            btn(area, siguiente_dict, eventos, font)

        if not juego_ganado:
            # Si el juego todavía no se ganó, se renderiza el botón de 'Volver'
            render_el(area, eventos, volver_dict, font)
        else:
            # Si el juego se ganó, mostramos un cartel del felicitaciones y un input para cargar el nombre del jugador
            elementos = [
                wrap_texto({"valor": "¡FELICITACIONES!"}, font),
                wrap_texto({"valor": f"Ganaste el juego con {get_estado("score")} puntos"}, font),
                wrap_texto({"valor": "Ingresá tu nombre:"}, font),
                wrap_input({"valor": get_estado("nombre_jugador")}, font),
                wrap_boton({"valor": "Cargar puntos", "callback": lambda: trigger("nombre_cargado")}, font)
            ]

            recuadro = wrap_recuadro(elementos, padding=(40, 20), gap=20, direccion="vertical", font=font)

            # Centramos el recuadro en pantalla
            x = (ANCHO - recuadro["ancho"]) // 2
            y = (ALTO - recuadro["alto"]) // 2
            recuadro["render"](area, (x, y), eventos)

    # PANTALLA ESTADÍSTICAS 👇
    elif pantalla == "estadisticas":
        estadisticas = leer_estadisticas()
        render_el(area, eventos, pant_estadisticas[0], font)
        wrappeables = [] # Preparamos un array de componentes que se renderizarán de manera estándar por un contenedor
        for el in pant_estadisticas[1:]:
            if el["tipo"] == "texto":
                wrappeables.append(wrap_texto({"valor": el["valor"]}, font))
        for i, jugador in enumerate(estadisticas):
            wrappeables.append(wrap_texto({"valor": f"{i + 1}. {jugador}"}, font))
        if not wrappeables:
            wrappeables = [wrap_texto({"valor": "Aún no hay estadísticas cargadas"}, font)]
        recuadro = wrap_recuadro(wrappeables, padding=(40, 20), gap=10, direccion="vertical", jusfify="left", font=font)
        # Centramos el recuadro en pantalla
        x = (ANCHO - recuadro["ancho"]) // 2
        y = (ALTO - recuadro["alto"]) // 2
        recuadro["render"](area, (x, y), eventos)
        render_el(area, eventos, volver_dict, font)
    
    # PANTALLA CRÉDITOS 👇
    elif pantalla == "creditos":
        render_el(area, eventos, pant_creditos[0], font)
        wrappeables = [] # Preparamos un array de componentes que se renderizarán de manera estándar por un contenedor
        for el in pant_creditos[1:]:
            wrappeables.append(wrap_texto({"valor": el["valor"]}, font))
        recuadro = wrap_recuadro(wrappeables, padding=(20, 10), gap=0, direccion="vertical", jusfify="left", font=font)
        # Centramos el recuadro en pantalla
        x = (ANCHO - recuadro["ancho"]) // 2
        y = (ALTO - recuadro["alto"]) // 2
        recuadro["render"](area, (x, y), eventos)
        render_el(area, eventos, volver_dict, font)

