import pygame
from pygame import Surface
from pygame.font import Font
from constantes import COLOR_TEXTO, COLOR_BOTON
from componentes.boton import crear_boton, render_boton, manejar_click_boton
from utils import cambiar_pantalla
from componentes.texto import render_texto
from componentes.input import crear_input, render_input, manejar_click_input

def render_pantalla(
    area: Surface,
    elementos: list[dict],
    eventos: list[pygame.event.Event],
    volver: bool = False,
    font: pygame.font.Font = None
) -> None:
    botones = []
    inputs = []
    for el in elementos:
        if el["tipo"] == "texto":
            render_texto(area, el, font)
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

    for boton in botones:
        render_boton(area, boton)
        manejar_click_boton(boton, eventos)
    for input in inputs:
        render_input(area, input)
        manejar_click_input(input, eventos)