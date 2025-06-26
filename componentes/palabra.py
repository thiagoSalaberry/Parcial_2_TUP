import pygame
from pygame.font import Font
from pygame import Surface
from constantes import COLOR_TEXTO
from componentes.input import crear_input, render_input, manejar_click_input
from estado import estado, set_estado


def mostrar_palabra(
    area: Surface,
    x: int,
    y: int,
    i_palabra: int,
    seleccionada: bool,
    callback: callable,
    eventos: pygame.event.Event,
    palabra_correcta: str,
    font: Font = None
) -> None:
    if font is None:
        font = pygame.font.SysFont(None, 24)

    palabras_completadas = estado["palabras_completadas"]
    score = estado["score"]
    palabra = palabras_completadas[i_palabra]

    bien = palabra == palabra_correcta
    mal = len(palabra) == 4 and palabra != palabra_correcta

    if mal:
        estado_palabra = "mal"
    elif bien:
        estado_palabra = "bien"
    else: 
        estado_palabra = "neutral"

    inputs = []
    for i in range(4):
        if i < len(palabra):
            letra = palabra[i]
        else:
            letra = ""
        input = crear_input(x + (i + i * 70), y, letra, seleccionada, estado_palabra, callback)
        inputs.append(input)
    
    for input in inputs:
        render_input(area, input)
        manejar_click_input(input, eventos)