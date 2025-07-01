import pygame
from pygame import Surface
from pygame.font import Font
from componentes.boton import boton as button
from interfaz_grafica.utils_pygame import leer_niveles
from componentes.texto import *
from interfaz_grafica.estado import get_estado, set_estado
from componentes.palabra import palabra
from interfaz_grafica.utils_pygame import *
from interfaz_grafica.pantallas import pant_estadisticas, pant_creditos
from ui.boton import wrap_palabra, wrap_boton, wrap_texto
from ui.input import wrap_input
from ui.recuadro import wrap_recuadro
from consola.funciones import leer_estadisticas
import sys


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