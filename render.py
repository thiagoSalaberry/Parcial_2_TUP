import pygame
from pygame import Surface
from pygame.font import Font
from constantes import COLOR_TEXTO, COLOR_BOTON
from componentes.boton import crear_boton, boton, manejar_click_boton
from utils.utils_pygame import cambiar_pantalla, leer_niveles
from componentes.texto import *
from componentes.input import crear_input, render_input, manejar_click_input
from estado import get_estado, set_estado
from componentes.palabra import palabra
from utils.utils_pygame import *
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
    pantalla, nivel_actual, estado_nivel_actual, palabras, palabras_completadas = get_estado("pantalla"), get_estado("nivel_actual"), get_estado("estado_nivel_actual"), get_estado("palabras"), get_estado("palabras_completadas")
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
    if pantalla == "jugar":
        nivel = {"tipo": "texto", "valor": nivel_actual, "pos": (50, 100)}
        els.append(nivel)
        if estado_nivel_actual == "ganado":
            boton_siguiente = {
                "tipo": "boton",
                "valor": "Siguiente nivel",
                "pos": (50, 500),
                "callback": lambda: siguiente_nivel(nivel_actual)
            }
            els.append(boton_siguiente)

    def render_el(area: Surface, eventos: list[pygame.event.Event], el: dict, **kwargs) -> None:
        match el["tipo"]:
            case "texto":
                texto(area, el, font)
            case "boton":
                boton(area, el, eventos)
            case "palabra":
                palabra(area, eventos, el)


    for el in els:
        render_el(area, eventos, el)
    # botones = []
    # inputs = []
    # if pantalla != "jugar":
    #     for el in els:
    #         if el["tipo"] == "texto":
    #             texto(area, el, font)
    #         elif el["tipo"] == "boton":
    #             x, y = el["pos"]
    #             boton = crear_boton(x, y, el["valor"], el["callback"], font=font)
    #             botones.append(boton)
    #         elif el["tipo"] == "input":
    #             x, y = el["pos"]
    #             input = crear_input(x, y, el["valor"], False, el["callback"])
    #             inputs.append(input)
    #         elif el["tipo"] == "pantalla":
    #             x, y = el["pos"]
    #             # crear_palabra(area, x, y, el["valor"], False, lambda: cambiar_pantalla("pantalla", "inicio"), eventos)

    #     estado_nivel_actual = get_estado("estado_nivel_actual")
    #     if estado_nivel_actual == "ganado":
    #         nivel_actual = get_estado("nivel_actual")
    #         boton_siguiente = crear_boton(500, 150, "Siguiente nivel", lambda: print(nivel_actual))
    #         botones.append(boton_siguiente)

        
    #     for boton in botones:
    #         boton(area, boton)
    #         manejar_click_boton(boton, eventos)
    #     for input in inputs:
    #         render_input(area, input)
    #         manejar_click_input(input, eventos)
    # else:
    #     palabras_correctas = get_estado("palabras")
    #     for i, palabra in enumerate(palabras_correctas):
    #         palabra(area, eventos, palabra, i, (40, i + 60 * i), font)

def render_nivel(area: Surface, events: list[pygame.event.Event], font: Font):
    nivel_actual = get_estado("nivel_actual")
    data_niveles = leer_niveles()
    datos_nivel = data_niveles[nivel_actual]
    palabras = datos_nivel["palabras"]
    pistas = datos_nivel["pistas"]

    for i, palabra in enumerate(palabras):
        pos = (100, i + i * 70)
        palabra(
            area=area,
            eventos=events,
            palabra_correcta=palabra,
            i=i,
            pos=pos,
            font=font
        )

