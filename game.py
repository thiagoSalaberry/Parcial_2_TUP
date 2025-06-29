import pygame
import os
import sys
from estado import get_estado, set_estado
from render import *
from eventos import on
from utils.utils_pygame import handle_level_change
from ui.boton import *

def main() -> None:
    # os.system("cls")
    pygame.init()
    pygame.mixer.init()
   
    # sound("inicio")

    ancho, alto = 800, 600

    screen = pygame.display.set_mode((ancho, alto))

    pygame.display.set_caption("CODY CROSS")
    clock = pygame.time.Clock()
    ejecutando = True

    font = pygame.font.Font("assets/font.ttf", 24)
    fondo = pygame.image.load("assets/fondo.png").convert()
    fondo = pygame.transform.scale(fondo, screen.get_size())

    # Inicializamos el estado
    data_niveles = leer_niveles()
    set_estado({
        "pantalla": "jugar",
        "nivel_actual": "dificil",
        "estado_nivel_actual": "jugando",
        "palabras": data_niveles["dificil"]["palabras"],
        "palabras_validadas": [False] * 8,
        "palabras_completadas": [""] * 8,
        "acertadas": [False] * 8,
        "pistas": data_niveles["dificil"]["pistas"]
    })   

    # Cargamos los eventos
    on("palabra_completada", handle_points)
    on("nivel_ganado", handle_win_level)
    on("cambio_de_nivel", handle_level_change)
    on("juego_ganado", handle_win_game)

    # Bucle principal del juego
    abc = "abcdefghijklmnñopqrstuvwxyz"
    while ejecutando:
        # 👇 Acá manejamos los eventos de teclado y mouse
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                pantalla, estado_nivel_actual = get_estado("pantalla"), get_estado("estado_nivel_actual")
                if pantalla == "jugar" and estado_nivel_actual == "jugando":
                    if event.key == pygame.K_TAB:
                        siguiente()
                    elif event.key == pygame.K_BACKSPACE:
                        borrar_letra()
                    else:
                        code = event.unicode
                        if code in "12345678":
                            set_estado({ "i_palabra_actual": int(code) - 1 })
                        else:
                            ingresar_letra(code.upper())

        screen.blit(fondo, (0, 0))
        pantalla, juego_ganado = get_estado("pantalla"), get_estado("juego_ganado")
        if pantalla != "inicio":
            overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # 128 = 0.5 de opacidad

            # Blittear la capa encima del fondo
            screen.blit(overlay, (0, 0))
        # render_pantalla(screen, events, font)

        i_palabra_actual, palabras, palabras_completadas = get_estado("i_palabra_actual"), get_estado("palabras"), get_estado("palabras_completadas")

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
            y = 54 * i
            palabra["render"](screen, (x, y), events)
        
        pygame.display.flip()
        clock.tick(60)

main()