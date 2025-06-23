import pygame
import sys
from pygame import Surface
from pygame.font import Font
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
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        screen.fill((20, 20, 20))

        # De acá para abajo 👇
        pantalla = estado["pantalla"]
        
        if pantalla == "home":
            render_menu(screen, events, font)
        elif pantalla == "jugar":
            render_pantalla(screen, pant_jugar, events, "home", fuente=font)
        elif pantalla == "estadisticas":
            render_pantalla(screen, pant_estadisticas, events, "home", fuente=font)
        elif pantalla == "creditos":
            render_pantalla(screen, pant_creditos, events, "home", fuente=font)

        pygame.display.flip()
        clock.tick(60)

play()


estado = {
    "pantalla": "home",
    "score": 0,
    "nivel_actual": "facil",
    "i_palabra_actual": 0,
    "palabras_completadas": [],
    "palabras": [],
    "pistas": [],
}

def set_estado(campo: str, valor: any) -> dict:
    if campo not in estado.keys():
        print(f"⚠️  El campo {campo} no pertenece al estado")
        return estado
    if type(valor) is not type(estado[campo]):
        print(f"⚠️  El tipo de dato de valor '{type(valor)}' es distinto al tipo del campo {campo} ({type(campo)})")
        return estado
    estado[campo] = valor
    return estado

def on_click_jugar() -> None:
    print("¡A jugar!")

def on_click_stats() -> None:
    print("A ver esas statssss")

def on_click_creditos() -> None:
    print("Quién hizo esta mierda??")

def on_click_salir() -> None:
    print("Hasta la próximaaa")
    pygame.quit()
    sys.exit(0)


def cambiar_pantalla(pantalla: str) -> None:
    set_estado("pantalla", pantalla)

def render_menu(screen: pygame.Surface, events: list[pygame.event.Event], fuente: pygame.font.Font) -> list[dict]:
    botones = [
        crear_boton(100, 150, "Jugar", lambda: cambiar_pantalla("jugar"), font=fuente),
        crear_boton(100, 220, "Estadísticas", lambda: cambiar_pantalla("estadisticas"), font=fuente),
        crear_boton(100, 290, "Créditos", lambda: cambiar_pantalla("creditos"), font=fuente),
        crear_boton(100, 360, "Salir", on_click_salir, font=fuente),
    ]

    for boton in botones:
        draw_boton(screen, boton)
        handle_boton_click(boton, events)
    # return botones

def render_pantalla(screen: pygame.Surface, elementos: list[dict], events: list[pygame.event.Event], volver_a: callable, fuente) -> list[dict]:
    for el in elementos:
        render_el(screen, el["tipo"], el, fuente)

    boton_volver = crear_boton(100, 400, "Volver", lambda: cambiar_pantalla(volver_a), font=fuente)
    draw_boton(screen, boton_volver)
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if boton_volver["rect"].collidepoint(event.pos):
                boton_volver["callback"]()
    
    return [boton_volver]



COLOR_TEXTO = (255, 255, 255)
COLOR_BOTON = (50, 50, 50)

def crear_boton(
    x: int,
    y: int,
    text: str,
    callback: callable,
    tipo_ancho: str = "auto",
    ancho_fijo: int = 100,
    padding_x: int = 20,
    padding_y: int = 10,
    font: Font = None,
) -> dict:
    if font is None:
        font = pygame.font.SysFont(None, 36)
    
    text_surface = font.render(text, True, (COLOR_TEXTO))
    text_rect = text_surface.get_rect()

    if tipo_ancho == "auto":
        ancho = text_rect.width + padding_x * 2
    else:
        ancho = ancho_fijo

    alto = text_rect.height + padding_y * 2

    rect = pygame.Rect(x, y, ancho, alto)

    return {
        "text": text,
        "rect": rect,
        "callback": callback,
        "text_surface": text_surface,
        "font": font,
    }

def draw_boton(surface: Surface, boton: dict) -> None:
    rect: pygame.Rect = boton["rect"]
    pygame.draw.rect(surface, COLOR_BOTON, rect, border_radius=5)
    surface.blit(
        boton["text_surface"],
        (
            rect.centerx - boton["text_surface"].get_width() // 2,
            rect.centery - boton["text_surface"].get_height() // 2
        )
    )


def handle_boton_click(boton: dict, events: list[pygame.event.Event]) -> None:
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if boton["rect"].collidepoint(event.pos):
                boton["callback"]()

def render_el(
    screen: pygame.Surface,
    tipo: str,
    el: dict,
    callback: callable = None,
    fuente: pygame.font.Font = None
) -> None:
    if fuente is None:
        fuente = pygame.font.SysFont(None, 36)

    if tipo == "texto":
        render_text(screen, el, fuente)
    elif tipo == "boton":
        render_boton(screen, el)

def render_boton(surface: pygame.Surface, boton: dict) -> None:
    rect: pygame.Rect = boton["rect"]
    pygame.draw.rect(surface, (255, 200, 200), rect, border_radius=5)
    surface.blit(
        boton["text_surface"],
        (
            rect.centerx - boton["text_surface"].get_width() // 2,
            rect.centery - boton["text_surface"].get_height() // 2
        )
    )

def render_text(screen: pygame.Surface, text_el: dict, font: pygame.font.Font = None) -> None:
    if font is None:
        font = pygame.font.SysFont(None, 36)
    
    x, y = text_el["pos"]
    texto = font.render(text_el["valor"], True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(x, y))
    
    screen.blit(texto, texto_rect)
        