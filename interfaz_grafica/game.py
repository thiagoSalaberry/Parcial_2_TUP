import os
import sys
import pygame
from estado import get_estado, set_estado
from eventos import on
from utils import leer_niveles, cargar_estadisticas
from funcs import manejar_puntos, ganar_nivel, cambiar_nivel, ganar_juego, borrar_letra, ingresar_letra, siguiente, sound
from render_funcs import render_pantalla
from constantes import ASSETS_PATH


def main() -> None:
    """
    Punto de entrada del juego.
    Define las variables principales, inicializa el estado central, carga los eventos, maneja las entradas del teclado y el mouse y renderiza las pantallas según el estado.
    Args:
        None
    Returns:
        None
    """
    os.system("cls")
    pygame.init()
    pygame.mixer.init()
   
    sound("inicio")

    ancho, alto = 800, 600

    screen = pygame.display.set_mode((ancho, alto))

    pygame.display.set_caption("CODY CROSS")
    clock = pygame.time.Clock()
    ejecutando = True

    font = pygame.font.Font(ASSETS_PATH + "/font.ttf", 24)
    fondo = pygame.image.load(ASSETS_PATH + "/fondo.png").convert()
    fondo = pygame.transform.scale(fondo, screen.get_size())

    # Inicializamos el estado
    data_niveles = leer_niveles()
    set_estado({
        "pantalla": "inicio",
        "nivel_actual": "facil",
        "estado_nivel_actual": "jugando",
        "palabras": data_niveles["facil"]["palabras"],
        "palabras_validadas": [False] * 8,
        "palabras_completadas": [""] * 8,
        "acertadas": [False] * 8,
        "pistas": data_niveles["facil"]["pistas"],
    })   

    # Cargamos los eventos
    on("palabra_completada", manejar_puntos)
    on("nivel_ganado", ganar_nivel)
    on("cambio_de_nivel", cambiar_nivel)
    on("juego_ganado", ganar_juego)
    on("nombre_cargado", cargar_estadisticas)  

    # Bucle principal del juego
    while ejecutando:
        # 👇 Acá manejamos los eventos de teclado y mouse
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                pantalla, estado_nivel_actual, juego_ganado, nombre_jugador = get_estado("pantalla"), get_estado("estado_nivel_actual"), get_estado("juego_ganado"), get_estado("nombre_jugador")
                if pantalla == "jugar" and juego_ganado:
                    code = event.unicode
                    if event.key == pygame.K_BACKSPACE:
                        borrar_letra("nombre_jugador")
                    else:
                        ingresar_letra(code.upper(), "nombre_jugador")
                elif pantalla == "jugar" and estado_nivel_actual == "jugando":
                    if event.key == pygame.K_TAB:
                        siguiente()
                    elif event.key == pygame.K_BACKSPACE:
                        borrar_letra("palabra_actual")
                    else:
                        code = event.unicode
                        print(code)
                        if code in "12345678":
                            set_estado({ "i_palabra_actual": int(code) - 1 })
                        else:
                            if code in "abcdefghijklmnñopqrstuvwxyz":
                                ingresar_letra(code.upper(), "palabra_actual")


        # Renderizamos la imagen de fondo
        screen.blit(fondo, (0, 0))

        # Agregamos un overlay transparente para mayor claridad durante el juego
        pantalla = get_estado("pantalla")
        if pantalla != "inicio":
            overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # 128 = 0.5 de opacidad

            screen.blit(overlay, (0, 0))

        # Esta es la función que se encarga de renderizar cada una de las pantallas
        render_pantalla(screen, events, font)
        
        pygame.display.flip()
        clock.tick(60)

main()