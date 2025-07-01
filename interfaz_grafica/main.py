import os
import sys
import pygame
from estado import get_estado, set_estado
from eventos import on
from utils import leer_niveles, cargar_estadisticas
from funcs import manejar_puntos, ganar_nivel, cambiar_nivel, cambiar_palabra, ganar_juego, borrar_letra, ingresar_letra, siguiente, sound
from render_funcs import render_pantalla
from constantes import ASSETS_PATH, ANCHO, ALTO


def main() -> None:
    """
    Punto de entrada del juego.
    Define las variables principales, inicializa el estado central, carga los eventos, maneja las entradas del teclado y el mouse y renderiza las pantallas según el estado.
    """
    os.system("cls")
    pygame.init()
    pygame.mixer.init()
   
    sound("inicio")

    screen = pygame.display.set_mode((ANCHO, ALTO))

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
        "nivel_actual": "dificil",
        "estado_nivel_actual": "jugando",
        "palabras": data_niveles["dificil"]["palabras"],
        "palabras_validadas": [False] * 8,
        "palabras_completadas": [""] * 8,
        "acertadas": [False] * 8,
        "pistas": data_niveles["dificil"]["pistas"],
    })   

    # Cargamos los eventos
    on("palabra_completada", manejar_puntos)
    on("nivel_ganado", ganar_nivel)
    on("cambio_de_nivel", cambiar_nivel)
    on("juego_ganado", ganar_juego)
    on("nombre_cargado", cargar_estadisticas)  

    # Limitamos las teclas posibles para que el juego no se rompa
    letras_validas = [pygame.K_a + i for i in range(26)]
    numeros_validos = [pygame.K_1 + i for i in range(8)]
    teclas_especiales = [pygame.K_BACKSPACE, pygame.K_TAB]
    teclas_validas = set(letras_validas + numeros_validos + teclas_especiales)

    # Bucle principal del juego
    while ejecutando:
        # 👇 Acá manejamos los eventos de teclado y mouse
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key in teclas_validas:
                    tecla = event.unicode
                    pantalla, estado_nivel_actual, juego_ganado = get_estado("pantalla"), get_estado("estado_nivel_actual"), get_estado("juego_ganado")

                    if pantalla == "jugar" and juego_ganado:
                        # Si el juego terminó, lo que hay que cargar es el nombre del jugador
                        if event.key == pygame.K_BACKSPACE:
                            borrar_letra("nombre_jugador")
                        else:
                            ingresar_letra(tecla.upper(), "nombre_jugador")
                    elif pantalla == "jugar" and estado_nivel_actual == "jugando":
                        # Si el juego NO terminó, lo que hay que cargar es la palabra actual
                        if event.key == pygame.K_TAB:
                            siguiente()
                        elif event.key == pygame.K_BACKSPACE:
                            borrar_letra("palabra_actual")
                        elif tecla in "12345678":
                            cambiar_palabra(int(tecla) - 1)
                        else:
                            ingresar_letra(tecla.upper(), "palabra_actual")

        # Renderizamos la imagen de fondo
        screen.blit(fondo, (0, 0))

        # Agregamos un overlay transparente para mayor claridad durante el juego
        pantalla = get_estado("pantalla")
        if pantalla != "inicio":
            overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # 128 = 0.5 de opacidad

            screen.blit(overlay, (0, 0))

        # Esta es la función que se encarga de renderizar cada una de las pantallas
        render_pantalla(screen, events, font)
        
        pygame.display.flip()
        clock.tick(60)

main()