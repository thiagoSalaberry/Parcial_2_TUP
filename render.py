import pygame
from pygame import Surface
from pygame.font import Font
from constantes import COLOR_TEXTO, COLOR_BOTON
from componentes.boton import crear_boton, boton as button, manejar_click_boton
from utils.utils_pygame import cambiar_pantalla, leer_niveles
from componentes.texto import *
from componentes.input import crear_input, render_input, manejar_click_input
from estado import get_estado, set_estado
from componentes.palabra import palabra
from utils.utils_pygame import *
from pantallas import pant_inicio, pant_jugar, pant_estadisticas, pant_creditos
from ui.boton import wrap_palabra
import sys


data_niveles = leer_niveles()
els_pantallas = {
    "inicio": [
        { "tipo": "texto", "valor": "Inicio", "pos": (300, 50) },
        { "tipo": "boton", "valor": "Jugar",        "pos": (400, 200), "callback": lambda: cambiar_pantalla("jugar") },
        { "tipo": "boton", "valor": "Estadísticas", "pos": (400, 260), "callback": lambda: cambiar_pantalla("estadisticas") },
        { "tipo": "boton", "valor": "Créditos",     "pos": (400, 320), "callback": lambda: cambiar_pantalla("creditos") },
        { "tipo": "boton", "valor": "Salir",        "pos": (400, 380), "callback": lambda: sys.exit(0) },
    ],
    "jugar": [
        { "tipo": "boton",  "valor": "Volver",   "pos": (690, 550), "callback": lambda: cambiar_pantalla("inicio") },
    ],
    "estadisticas": [
        { "tipo": "texto",  "valor": "Ranking", "pos": (400, 45) },
        { "tipo": "texto",  "valor": "1 - Mateo", "pos": (400, 85) },
        { "tipo": "texto",  "valor": "2 - Valentina", "pos": (400, 125) },
        { "tipo": "texto",  "valor": "3 - Thiago", "pos": (400, 165) },
        { "tipo": "texto",  "valor": "4 - Isabella", "pos": (400, 205) },
        { "tipo": "texto",  "valor": "5 - Benjamín", "pos": (400, 245) },
        { "tipo": "texto",  "valor": "6 - Sofía", "pos": (400, 285) },
        { "tipo": "texto",  "valor": "7 - Santiago", "pos": (400, 325) },
        { "tipo": "texto",  "valor": "8 - Emma", "pos": (400, 365) },
        { "tipo": "texto",  "valor": "9 - Joaquín", "pos": (400, 405) },
        { "tipo": "texto",  "valor": "10 - Olivia", "pos": (400, 445) },
        { "tipo": "boton",  "valor": "Volver",                  "pos": (690, 550), "callback": lambda: cambiar_pantalla("inicio") },
    ],
    "creditos": [
        { "tipo": "texto",  "valor": "Créditos", "pos": (400, 45) },
        { "tipo": "texto",  "valor": "Autores:", "pos": (400, 75) },
        { "tipo": "texto",  "valor": "Bautista Ruiz", "pos": (400, 105) },
        { "tipo": "texto",  "valor": "Thiago Salaberryz", "pos": (400, 125) },
        { "tipo": "texto",  "valor": "Fecha de Desarrollo:", "pos": (400, 165) },
        { "tipo": "texto",  "valor": "Junio 2025", "pos": (400, 195) },
        { "tipo": "texto",  "valor": "Materia:", "pos": (400, 235) },
        { "tipo": "texto",  "valor": "Programación I", "pos": (400, 265) },
        { "tipo": "texto",  "valor": "Docente:", "pos": (400, 305) },
        { "tipo": "texto",  "valor": "Prof. Martín Alejandro García y Verónica Natalia Carbonari", "pos": (400, 335) },
        { "tipo": "texto",  "valor": "Carrera:", "pos": (400, 375) },
        { "tipo": "texto",  "valor": "Tecnicatura Universitaria en Programación - UTN Avellaneda", "pos": (400, 405) },
        { "tipo": "texto",  "valor": "Emails de contacto:", "pos": (400, 445) },
        { "tipo": "texto",  "valor": "bautyruiz1011@gmail.com", "pos": (400, 475) },
        { "tipo": "texto",  "valor": "thiagosalaberry99@gmail.com", "pos": (400, 505) },
        { "tipo": "boton",  "valor": "Volver",   "pos": (690, 550), "callback": lambda: cambiar_pantalla("inicio") },
    ],
    "test": [
        { "tipo": "texto",  "valor": "thiagosalaberry99@gmail.com", "pos": (400, 505) },
        { "tipo": "boton",  "valor": "Volver",   "pos": (690, 550), "callback": lambda: cambiar_pantalla("creditos") },
    ]
}
els_pantallas = {
    "inicio": pant_inicio,
    "jugar": pant_jugar,
    "estadisticas": pant_estadisticas,
    "creditos": pant_creditos,
}


def render_el(area: Surface, eventos: list[pygame.event.Event], el: dict, font: Font) -> None:
    match el["tipo"]:
        case "texto":
            texto(area, el, font)
        case "boton":
            button(area, el, eventos, font)
        case "palabra":
            palabra(area, eventos, el)


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
    els = []
    pantalla = get_estado("pantalla")
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
    elif pantalla == "jugar":
        palabras, palabras_completadas, i_palabra_actual, estado_nivel_actual = get_estado("palabras"), get_estado("palabras_completadas"), get_estado("i_palabra_actual"), get_estado("estado_nivel_actual")
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
            y = 100 + 54 * i
            palabra["render"](area, (x, y), eventos)
        if estado_nivel_actual == "ganado":
            siguiente_dict = { "tipo": "boton", "valor": "Siguiente nivel", "callback": siguiente_nivel, "pos": (500, 500) }
            button(area, siguiente_dict, eventos, font)
    elif pantalla == "estadisticas":
        els = pant_estadisticas
    elif pantalla == "creditos":
        els = pant_creditos
    
    if pantalla != "inicio":
        for el in els:
            render_el(area, eventos, el, font)

    return
    pantalla, nivel_actual, estado_nivel_actual, palabras, pistas, score, i_palabra_actual = get_estado("pantalla"), get_estado("nivel_actual"), get_estado("estado_nivel_actual"), get_estado("palabras"), get_estado("pistas"), get_estado("score"), get_estado("i_palabra_actual")
    els = els_pantallas[pantalla]

    if pantalla == "jugar":
        palabras_nivel = []
        for i, pal in enumerate(palabras):
            palabra_dict = {
                "tipo": "palabra",
                "valor": i,
                "correcta": pal,
                "pos": (100, 50 + 50 * i)
            }
            palabras_nivel.append(palabra_dict)
        els = els + palabras_nivel
        if nivel_actual == "facil":
            nivel_n = "1"
        if nivel_actual == "intermedio":
            nivel_n = "2"
        if nivel_actual == "dificil":
            nivel_n = "3"
        nivel = {"tipo": "texto", "valor": f"Nivel: {nivel_n}", "pos": (665, 30)}
        score = {"tipo": "texto", "valor": f"Puntos: {score}", "pos": (680, 50)}
        pista = {"tipo": "texto", "valor": f"{pistas[i_palabra_actual]}", "pos": (400, 530)}
        els.append(nivel)
        els.append(score)
        els.append(pista)
        if estado_nivel_actual == "ganado":
            boton_siguiente = {
                "tipo": "boton",
                "valor": "Siguiente nivel",
                "pos": (630, 550),
                "callback": siguiente_nivel
            }
            els.append(boton_siguiente)

    for el in els:
        render_el(area, eventos, el, font)