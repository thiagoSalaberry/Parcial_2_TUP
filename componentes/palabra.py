import pygame
from pygame.font import Font
from pygame import Surface
from constantes import COLOR_TEXTO
from componentes.input import crear_input, render_input, manejar_click_input
from estado import estado, set_estado, get_estado


def ir_a_palabra(i: int) -> None:
    acertadas = get_estado("acertadas")
    if not acertadas[i]:
        set_estado({ "i_palabra_actual": i })


def palabra(
    area: Surface,
    eventos: list[pygame.event.Event],
    palabra_el: dict,
    font: Font = None
) -> None:
    if not font:
        font = pygame.font.SysFont(None, 24)

    palabra_correcta, i, pos = palabra_el["correcta"], palabra_el["valor"], palabra_el["pos"]
    palabras, palabras_completadas, i_palabra_actual = get_estado("palabras"), get_estado("palabras_completadas"), get_estado("i_palabra_actual")
    palabra = palabras_completadas[i]

    bien = palabra == palabra_correcta
    mal = len(palabra) == len(palabras[0]) and palabra != palabra_correcta

    if bien:
        estado_palabra = "bien"
    elif mal:
        estado_palabra = "mal"
    else:
        estado_palabra = "neutral"

    x, y = pos
    letras = []
    for j in range(len(palabra_correcta)):
        if j < len(palabra):
            char = palabra[j]
        else:
            char = ""
        letra = crear_input(x + (x + j * 70), y, char, i == i_palabra_actual, estado_palabra, lambda: ir_a_palabra(i), font)
        letras.append(letra)

    for letra in letras:
        render_input(area, letra)
        manejar_click_input(letra, eventos)
