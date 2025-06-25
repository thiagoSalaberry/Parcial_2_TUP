import pygame
import sys
from pygame import Surface
from pygame.font import Font
from estado import estado, set_estado
from pantallas_modelo import pant_creditos, pant_estadisticas, pant_inicio, pant_jugar
from render import render_pantalla
from componentes.palabra import mostrar_palabra
from componentes.texto import render_texto


def cambiar_pantalla(pantalla: str) -> None:
    set_estado("pantalla", pantalla)

def ingresar_palabra(i_palabra: int, palabra: str) -> None:
    palabras_completadas = estado["palabras_completadas"]
    palabras_completadas[i_palabra] = palabra
    set_estado("palabras_completadas", palabras_completadas)

COLOR_TEXTO = (255, 255, 255)
COLOR_BOTON = (50, 50, 50)

palabras = [
    { "palabra": "PESO", "seleccionado": estado["i_palabra_actual"] == 0 },
    { "palabra": "ASNO", "seleccionado": estado["i_palabra_actual"] == 1 },
    { "palabra": "ECHA", "seleccionado": estado["i_palabra_actual"] == 2 },
    { "palabra": "CAMA", "seleccionado": estado["i_palabra_actual"] == 3 },
    { "palabra": "ALTO", "seleccionado": estado["i_palabra_actual"] == 4 },
    { "palabra": "BEBÉ", "seleccionado": estado["i_palabra_actual"] == 5 },
    { "palabra": "ARCO", "seleccionado": estado["i_palabra_actual"] == 6 },
    { "palabra": "CAJA", "seleccionado": estado["i_palabra_actual"] == 7 },
]
pistas = [
    "Cantidad que marca la balanza o lo que llevás cargado",
    "Mamífero doméstico, pariente del caballo, famoso por su terquedad",
    "Forma del verbo “echar” en tercera persona",
    "Mueble donde se duerme o descansa",
    "Que tiene gran altura o intensidad",
    "Niño muy pequeño",
    "Instrumento para disparar flechas",
    "Recipiente con tapa para guardar o transportar objetos"
]

def play():
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

    while ejecutando:
        palabras_completadas = estado["palabras_completadas"]
        palabra_actual = palabras_completadas[estado["i_palabra_actual"]]   
        i_palabra_actual = estado["i_palabra_actual"]
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    palabra_actual = palabra_actual[:-1]
                    ingresar_palabra(i_palabra_actual, palabra_actual)
                elif event.key == pygame.K_TAB:
                    set_estado("i_palabra_actual", i_palabra_actual + 1 if i_palabra_actual < 7 else 0)
                else:
                    if len(palabra_actual) < 4:
                        palabra_actual += event.unicode.upper()
                        ingresar_palabra(i_palabra_actual, palabra_actual)
                print(palabra_actual)
        screen.fill((20, 20, 20))

        # De acá para abajo 👇
        pantalla = estado["pantalla"]
        
        if pantalla == "inicio":
            for i, palabra in enumerate(palabras):
                mostrar_palabra(
                    screen,
                    200,
                    i + i * 70,
                    i,
                    estado["i_palabra_actual"] == i,
                    lambda: set_estado("i_palabra_actual", i),
                    events,
                    palabra["palabra"]
                )
            texto = { "tipo": "texto",  "valor": pistas[estado["i_palabra_actual"]], "pos": (400, 500) }
            render_texto(screen, texto)
            
        elif pantalla == "jugar":
            render_pantalla(screen, pant_jugar, events, volver=True, font=font)
        elif pantalla == "estadisticas":
            render_pantalla(screen, pant_estadisticas, events, volver=True, font=font)
        elif pantalla == "creditos":
            render_pantalla(screen, pant_creditos, events, volver=True, font=font)

        pygame.display.flip()
        clock.tick(60)

play()