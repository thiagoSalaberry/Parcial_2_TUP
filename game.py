import pygame
import os
import sys
from pygame import Surface
from pygame.font import Font
from estado import estado, get_estado, set_estado, subscribe
from pantallas import pant_creditos, pant_estadisticas, pant_inicio, pant_jugar
from render import *
from componentes.boton import *
from componentes.texto import texto
from constantes import ARCH_NIVELES
from eventos import on, trigger
from utils.utils_pygame import handle_level_change
import json


COLOR_TEXTO = (9, 5, 250)
COLOR_BOTON = (245, 206, 10)


def main() -> None:
    os.system("cls")
    pygame.init()
    pygame.mixer.init()
   
    sound("inicio")
    
    

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
        "pantalla": "inicio",
        "nivel_actual": "facil",
        "estado_nivel_actual": "jugando",
        "palabras": data_niveles["facil"]["palabras"],
        "palabras_validadas": [False] * 8,
        "palabras_completadas": [""] * 8,
        "acertadas": [False] * 8,
        "pistas": data_niveles["facil"]["pistas"]
    })   

    on("palabra_completada", handle_points)
    on("nivel_ganado", handle_win)
    on("hola", lambda: print("hola"))
    on("chau", lambda: print("chau"))
    on("cambio_de_nivel", handle_level_change)
    pantalla = get_estado("pantalla")
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

        render_pantalla(screen, events, font)

        pygame.display.flip()
        clock.tick(60)

main()