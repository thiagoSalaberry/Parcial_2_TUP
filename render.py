import pygame
from pygame import Surface
from pygame.font import Font
from constantes import COLOR_TEXTO, COLOR_BOTON
from componentes.boton import crear_boton, render_boton, manejar_click_boton
from utils.utils_pygame import cambiar_pantalla, leer_niveles
from componentes.texto import *
from componentes.input import crear_input, render_input, manejar_click_input
from estado import get_estado
from componentes.palabra import rn_palabra
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
    "jugar": {
        "facil": {
            "palabras": data_niveles["facil"]["palabras"],
            "pistas": data_niveles["facil"]["pistas"]
        },
        "intermedio": {
            "palabras": data_niveles["intermedio"]["palabras"],
            "pistas": data_niveles["intermedio"]["pistas"]
        },
        "dificil": {
            "palabras": data_niveles["dificil"]["palabras"],
            "pistas": data_niveles["dificil"]["pistas"]
        },
    },
    "estadisticas": [
        { "tipo": "texto", "valor": "Ranking", "pos": (300, 50) },
        { "tipo": "boton", "valor": "Volver",        "pos": (400, 200), "callback": lambda: cambiar_pantalla("inicio") }
    ],
    "creditos": [
        { "tipo": "texto", "valor": "Créditos", "pos": (300, 50) },
        { "tipo": "boton", "valor": "Volver",        "pos": (400, 200), "callback": lambda: cambiar_pantalla("inicio") }

    ],
}

def render_pantalla(
    area: Surface,
    elementos: list[dict],
    eventos: list[pygame.event.Event],
    volver: bool = False,
    font: pygame.font.Font = None
) -> None:
    pantalla = get_estado("pantalla")
    els = els_pantallas[pantalla]
    botones = []
    inputs = []
    if pantalla != "jugar":
        for el in els:
            if el["tipo"] == "texto":
                texto(area, el, font)
            elif el["tipo"] == "boton":
                x, y = el["pos"]
                boton = crear_boton(x, y, el["valor"], el["callback"])
                botones.append(boton)
            elif el["tipo"] == "input":
                x, y = el["pos"]
                input = crear_input(x, y, el["valor"], False, el["callback"])
                inputs.append(input)
            elif el["tipo"] == "pantalla":
                x, y = el["pos"]
                # crear_palabra(area, x, y, el["valor"], False, lambda: cambiar_pantalla("pantalla", "inicio"), eventos)


                
        if volver:
            boton_volver = crear_boton(500, 50, "Volver", lambda: cambiar_pantalla("pantalla", "inicio"))
            botones.append(boton_volver)

        estado_nivel_actual = get_estado("estado_nivel_actual")
        if estado_nivel_actual == "ganado":
            nivel_actual = get_estado("nivel_actual")
            boton_siguiente = crear_boton(500, 150, "Siguiente nivel", lambda: print(nivel_actual))
            botones.append(boton_siguiente)

        
        for boton in botones:
            render_boton(area, boton)
            manejar_click_boton(boton, eventos)
        for input in inputs:
            render_input(area, input)
            manejar_click_input(input, eventos)

def render_nivel(area: Surface, events: list[pygame.event.Event], font: Font):
    nivel_actual = get_estado("nivel_actual")
    data_niveles = leer_niveles()
    datos_nivel = data_niveles[nivel_actual]
    palabras = datos_nivel["palabras"]
    pistas = datos_nivel["pistas"]

    for i, palabra in enumerate(palabras):
        pos = (100, i + i * 70)
        rn_palabra(
            area=area,
            eventos=events,
            palabra_correcta=palabra,
            i=i,
            pos=pos,
            font=font
        )

