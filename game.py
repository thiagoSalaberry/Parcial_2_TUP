import pygame
import os
import sys
from pygame import Surface
from pygame.font import Font
from estado import estado, get_estado, set_estado, subscribe
from pantallas_modelo import pant_creditos, pant_estadisticas, pant_inicio, pant_jugar
from render import render_pantalla
from componentes.palabra import mostrar_palabra
from componentes.texto import render_texto
from constantes import ARCH_NIVELES
import json

def cambiar_pantalla(pantalla: str) -> None:
    set_estado("pantalla", pantalla)

def ingresar_palabra(i_palabra: int, palabra: str) -> None:
    palabras_completadas = estado["palabras_completadas"]
    palabras_completadas[i_palabra] = palabra
    set_estado({
        "palabras_completadas": palabras_completadas
    })

COLOR_TEXTO = (255, 255, 255)
COLOR_BOTON = (50, 50, 50)


def leer_niveles(arch_niveles: str = ARCH_NIVELES) -> dict:
    with open(arch_niveles, "r", encoding="utf-8") as archivo_niveles:
        datos_niveles = json.load(archivo_niveles)
    
    return datos_niveles["niveles"]


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

    data_niveles = leer_niveles()

    # Inicializamos el estado
    set_estado({
        "pantalla": "inicio",
        "nivel_actual": "facil",
        "palabras": data_niveles["facil"]["palabras"],
        "palabras_validadas": [False] * 8,
        "palabras_completadas": ["", "", "", "", "", "", "", ""],
        "pistas": data_niveles["facil"]["pistas"]
    })
    
    def validar_palabra() -> None:
        palabras_completadas = estado["palabras_completadas"]
        palabras = estado["palabras"]
        i = estado["i_palabra_actual"]
        validadas = estado["palabras_validadas"]
        if len(palabras_completadas[i]) == 4:
            print(validadas)
            if not validadas[i]:
                validadas[i] = True
                set_estado({
                    "palabras_validadas": validadas
                })

    def handle_points() -> None:
        palabras_completadas = estado["palabras_completadas"]
        palabras = estado["palabras"]
        i = estado["i_palabra_actual"]
        validadas = estado["palabras_validadas"]

        if not validadas[i] and len(palabras_completadas[i]) == 4:
            if palabras_completadas[i] == palabras[i]:
                validadas[i] = True
                set_estado({
                    "score": estado["score"] + 10,
                    "palabras_validadas": validadas
                })
            else:
                # No se marca como validada, se espera a que el usuario corrija
                set_estado({
                    "score": estado["score"] - 5
                })
    def ingresar_letra(letra: str) -> None:
        i_palabra_actual = estado["i_palabra_actual"]
        palabra_actual = estado["palabras_completadas"][i_palabra_actual]
        if len(palabra_actual) < 4:
            palabra_actual += letra
            palabras_completadas[i_palabra_actual] = palabra_actual
            set_estado({
                "palabras_completadas": palabras_completadas,
                "palabra_actual": palabra_actual
            })
    def borrar_letra() -> None:
        i_palabra_actual = estado["i_palabra_actual"]
        palabra_actual = estado["palabras_completadas"][i_palabra_actual][:-1]
        palabras_completadas[i_palabra_actual] = palabra_actual
        validadas = estado["palabras_validadas"]
        validadas[i_palabra_actual] = False
        set_estado({
            "palabras_completadas": palabras_completadas,
            "palabra_actual": palabra_actual,
            "palabras_validadas": validadas
        })
    subscribe(validar_palabra)
    while ejecutando:
        pantalla, score, nivel_actual, i_palabra_actual, palabra_actual, palabras_completadas, palabras, palabras_validadas, pistas, listeners = estado.values()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    nuevo_i = i_palabra_actual + 1 if i_palabra_actual < 7 else 0
                    palabra_actual = palabras_completadas[nuevo_i]
                    set_estado({
                        "i_palabra_actual": nuevo_i,
                        "palabra_actual": palabra_actual
                    })
                elif event.key == pygame.K_BACKSPACE:
                    borrar_letra()
                else:
                    ingresar_letra(event.unicode.upper())
        screen.fill((20, 20, 20))

        # De acá para abajo 👇
        if pantalla == "inicio":
            for i in range(len(palabras)):
                mostrar_palabra(
                    screen,
                    200,
                    i + i * 70,
                    i,
                    estado["i_palabra_actual"] == i,
                    lambda: set_estado("i_palabra_actual", i),
                    events,
                    palabras[i]
                )
            texto_pista = { "tipo": "texto",  "valor": pistas[i_palabra_actual], "pos": (400, 500) }
            texto_score = { "tipo": "texto",  "valor": str(score), "pos": (50, 50) }
            render_texto(screen, texto_pista)
            render_texto(screen, texto_score)
            
        elif pantalla == "jugar":
            render_pantalla(screen, pant_jugar, events, volver=True, font=font)
        elif pantalla == "estadisticas":
            render_pantalla(screen, pant_estadisticas, events, volver=True, font=font)
        elif pantalla == "creditos":
            render_pantalla(screen, pant_creditos, events, volver=True, font=font)

        pygame.display.flip()
        clock.tick(60)

# play()

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

    estado = get_estado()
    data_niveles = leer_niveles()
    set_estado({
            "pantalla": "inicio",
            "nivel_actual": "facil",
            "palabras": data_niveles["facil"]["palabras"],
            "palabras_validadas": [False] * 8,
            "palabras_completadas": ["", "", "", "", "", "", "", ""],
            "pistas": data_niveles["facil"]["pistas"]
        })
    print(json.dumps(estado, indent=4))

    palabra = ""
    def print_palabra():
        os.system("cls")
        estado = get_estado()
        print(json.dumps(estado, indent=4))

    subscribe(print_palabra)

    def crear_letra(x: int, y: int, letra: str, activo: bool, estado: str, callback: callable, font: Font = None) -> dict:
        if not font:
            font = pygame.font.SysFont(None, 24)
        
        area_texto = font.render(letra, True, (255, 255, 255))        
        ancho, alto = 50, 50

        rect = pygame.Rect(x, y, ancho, alto)

        return {
            "letra": letra,
            "rect": rect,
            "activo": activo,
            "estado": estado,
            "callback": callback,
            "area_texto": area_texto,
        }

    def rn_letra(area: Surface, letra: dict) -> None:
        rect: pygame.Rect = letra["rect"]

        fondo = (40, 40, 40)

        pygame.draw.rect(area, fondo, rect)
        area.blit(
            letra["area_texto"],
            (
                rect.centerx - letra["area_texto"].get_width() // 2,
                rect.centery - letra["area_texto"].get_height() // 2,
            )
        )

    
    
    while ejecutando:
        # 👇 Acá manejamos los eventos de teclado y mouse
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    set_estado({
                        "palabra_actual": palabra
                    })
                elif event.key == pygame.K_BACKSPACE:
                    palabra = palabra[:-1]
                else:
                    code = event.unicode
                    if code in ["i", "j", "e", "c"]:
                        set_estado({ "pantalla": code })

        # Acá extraemos el valor de la pantalla que determinará qué pantalla vamos a renderizar
        pantalla = get_estado("pantalla")    
        if pantalla == "i":
            print("🏠 Inicio")
        elif pantalla == "j":
            print("🕹️ A Jugar")
        elif pantalla == "e":
            print("📊 Estadísticas")
        elif pantalla == "c":
            print("👨👨 Créditos")


        pygame.display.flip()
        clock.tick(60)

main()