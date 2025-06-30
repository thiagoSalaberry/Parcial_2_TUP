import pygame
import os
import sys
from estado import get_estado, set_estado
from render import *
from eventos import on
from utils.utils_pygame import handle_level_change
from ui.boton import *
from ui.recuadro import *
from ui.input import *
from funciones import leer_estadisticas
from constantes import ARCH_ESTAD as arch_estad
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
        "pantalla": "inicio",
        "nivel_actual": "facil",
        "estado_nivel_actual": "jugando",
        "palabras": data_niveles["facil"]["palabras"],
        "palabras_validadas": [False] * 8,
        "palabras_completadas": [""] * 8,
        "acertadas": [False] * 8,
        "pistas": data_niveles["facil"]["pistas"],
    })   

    def cargar_estadisticas() -> None:
        score = get_estado("score")
        estadisticas = leer_estadisticas(print=False)
        puntajes = [int(linea.split(" - ")[1]) for linea in estadisticas]
        if not puntajes or len(puntajes) < 10 or (len(puntajes) == 10 and score > puntajes[-1]):
            print("🎉 Entraste en el top 10")
            nombre_jugador = get_estado("nombre_jugador")
            estadisticas: list[str] = leer_estadisticas(print=False)

            estadisticas.append(f"{nombre_jugador} - {score}")
            estadisticas.sort(key=lambda x: int(x.split(" - ")[1]), reverse=True)

            with open(arch_estad, "w") as file:
                file.writelines([f"{linea}\n" for linea in estadisticas][:10])
            
        else:
            print("😞 NO entraste en el top 10")
        set_estado({"pantalla": "estadisticas"})
    # Cargamos los eventos
    on("palabra_completada", handle_points)
    on("nivel_ganado", handle_win_level)
    on("cambio_de_nivel", handle_level_change)
    on("juego_ganado", handle_win_game)
    on("nombre_cargado", cargar_estadisticas)

    
    
    

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
                        if code in "12345678":
                            set_estado({ "i_palabra_actual": int(code) - 1 })
                        else:
                            ingresar_letra(code.upper(), "palabra_actual")


        screen.blit(fondo, (0, 0))
        pantalla, juego_ganado = get_estado("pantalla"), get_estado("juego_ganado")
        if pantalla != "inicio":
            overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # 128 = 0.5 de opacidad

            # Blittear la capa encima del fondo
            screen.blit(overlay, (0, 0))
        render_pantalla(screen, events, font)
        if juego_ganado and pantalla == "jugar":
            elementos = [
                wrap_texto({"valor": "¡FELICITACIONES!"}, font),
                wrap_texto({"valor": f"Ganaste el juego con {get_estado("score")} puntos"}, font),
                wrap_texto({"valor": "Ingresá tu nombre:"}, font),
                wrap_input({"valor": get_estado("nombre_jugador")}, font),
                wrap_boton({"valor": "Cargar puntos", "callback": lambda: trigger("nombre_cargado")}, font)
            ]

            recuadro = wrap_recuadro(elementos, padding=(40, 20), gap=20, direccion="vertical", font=font)

            # Centramos el recuadro en pantalla
            x = (ancho - recuadro["ancho"]) // 2
            y = (alto - recuadro["alto"]) // 2
            recuadro["render"](screen, (x, y), events)
        
        pygame.display.flip()
        clock.tick(60)

main()