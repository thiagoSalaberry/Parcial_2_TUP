import pygame
from constantes import COLOR_TEXTO, COLOR_BOTON
from pygame import Surface

def crear_boton(
    x: int,
    y: int,
    texto: str,
    callback: callable,
    tipo_ancho: str = "auto",
    ancho_fijo: int = 100,
    padding_x: int = 20,
    padding_y: int = 10,
    font: pygame.font.Font = None
) -> dict:
    if font is None:
        font = pygame.font.SysFont(None, 24)

    area_texto = font.render(texto, True, COLOR_TEXTO)
    rect_texto = area_texto.get_rect()

    if tipo_ancho == "auto":
        ancho = rect_texto.width + padding_x * 2
    else:
        ancho = ancho_fijo

    alto = rect_texto.height + padding_y * 2

    rect = pygame.Rect(x, y, ancho, alto)

    return {
        "texto": texto,
        "rect": rect,
        "callback": callback,
        "area_texto": area_texto,
        "font": font
    }

def render_boton(area: Surface, boton: dict) -> None:
    rect: pygame.Rect = boton["rect"]
    pygame.draw.rect(area, COLOR_BOTON, rect, border_radius=5)
    area.blit(
        boton["area_texto"],
        (
            rect.centerx - boton["area_texto"].get_width() // 2,
            rect.centery - boton["area_texto"].get_height() // 2
        )
    )

def manejar_click_boton(boton: dict, eventos: list[pygame.event.Event]) -> None:
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton["rect"].collidepoint(evento.pos):
                boton["callback"]()