import pygame
from pygame.font import Font
from pygame import Surface
from constantes import COLOR_TEXTO


def crear_input(
    x: int,
    y: int,
    letra: str,
    activo: bool,
    estado_palabra: str,
    callback: callable,
    font: Font = None
) -> dict:
    if font is None:
        font = pygame.font.SysFont(None, 24)

    area_texto = font.render(letra, True, COLOR_TEXTO)

    ancho, alto = 60, 60

    rect = pygame.Rect(x, y, ancho, alto)

    return {
        "letra": letra,
        "rect": rect,
        "activo": activo,
        "estado_palabra": estado_palabra,
        "callback": callback,
        "area_texto": area_texto,
        "rect": rect
    }


def render_input(area: Surface, input: dict) -> None:
    rect: pygame.Rect = input["rect"]
    
    if input["estado_palabra"] == "bien":
        fondo = (100, 255, 100)
    elif input["estado_palabra"] == "mal":
        fondo = (255, 100, 100)
    elif input["activo"]:
        fondo = (100, 100, 100)
    else:
        fondo = (40, 40, 40)

    pygame.draw.rect(area, fondo, rect, border_radius=5)
    area.blit(
        input["area_texto"],
        (
            rect.centerx - input["area_texto"].get_width() // 2,
            rect.centery - input["area_texto"].get_height() // 2,
        )
    )


def manejar_click_input(input: dict, eventos: list[pygame.event.Event]) -> None:
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if input["rect"].collidepoint(evento.pos):
                input["callback"]()