import pygame
import os
import sys
from pygame import Surface
from pygame.font import Font
from estado import estado, get_estado, set_estado, subscribe
from pantallas import pant_creditos, pant_estadisticas, pant_inicio, pant_jugar
from render import render_pantalla
from componentes.palabra import rn_palabra
from componentes.texto import render_texto
from constantes import ARCH_NIVELES
from eventos import on, trigger
from utils.utils_pygame import *
import json


COLOR_TEXTO = (255, 255, 255)
COLOR_BOTON = (50, 50, 50)


def leer_niveles(arch_niveles: str = ARCH_NIVELES) -> dict:
    with open(arch_niveles, "r", encoding="utf-8") as archivo_niveles:
        datos_niveles = json.load(archivo_niveles)
    
    return datos_niveles["niveles"]


def main() -> None:
    os.system("cls")
    pygame.init()

    ancho = 800
    alto = 600
    color = (203, 219,  208)

    screen = pygame.display.set_mode((ancho, alto))

    pygame.display.set_caption("CODY CROSS")
    clock = pygame.time.Clock()
    ejecutando = True

    font = pygame.font.Font("assets/font.ttf", 24)
    fondo = pygame.image.load("assets/fondo.png").convert()
    fondo = pygame.transform.scale(fondo, screen.get_size())

    data_niveles = leer_niveles()
    set_estado({
        "pantalla": "test",
        "nivel_actual": "facil",
        "palabras": data_niveles["facil"]["palabras"],
        "palabras_validadas": [False] * 8,
        "palabras_completadas": ["", "", "", "", "", "", "", ""],
        "acertadas": [False] * 8,
        "pistas": data_niveles["facil"]["pistas"]
    })   

    on("palabra_completada", handle_points)
    on("nivel_ganado", handle_win)

    palabras = get_estado("palabras")
    while ejecutando:
        # 👇 Acá manejamos los eventos de teclado y mouse
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    i_palabra_actual = get_estado("i_palabra_actual")
                    siguiente(i_palabra_actual)
                elif event.key == pygame.K_BACKSPACE:
                    borrar_letra()
                else:
                    code = event.unicode
                    if code in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                        set_estado({ "i_palabra_actual": int(code) - 1 })
                    else:
                        ingresar_letra(code.upper())
                    
        screen.blit(fondo, (0, 0))

        # Acá extraemos el valor de la pantalla que determinará qué pantalla vamos a renderizar
        pantalla = get_estado("pantalla")    
        if pantalla == "inicio":
            render_pantalla(screen, pant_inicio, events, False, font)
        elif pantalla == "jugar":
            render_pantalla(screen, pant_jugar, events, False, font)
        elif pantalla == "estadisticas":
            render_pantalla(screen, pant_estadisticas, events, False, font)
        elif pantalla == "creditos":
            render_pantalla(screen, pant_creditos, events, False, font)
        else:
            for i, palabra in enumerate(palabras):
                pos = (100, i + i * 70)
                rn_palabra(
                    area=screen,
                    eventos=events,
                    palabra_correcta=palabra,
                    i=i,
                    pos=pos,
                    font=font
                )


        pygame.display.flip()
        clock.tick(60)

main()