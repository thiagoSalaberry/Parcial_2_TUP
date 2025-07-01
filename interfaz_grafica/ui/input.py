import pygame
from pygame.font import Font
from pygame.event import Event
from constantes import COLOR_LETRA_ACTIVO, COLOR_LETRA_ACTIVO_SOMBRA


def crear_input(texto: str, font: Font) -> dict:
    if font is None:
        font = pygame.font.SysFont(None, 24)

    area_texto = font.render(texto, True, (255, 255, 255))
    rect = pygame.Rect(0, 0, 200, 40)
    rect_sombra = pygame.Rect(0, 4, 200, 40)
    
    return {
        "texto": texto,
        "area_texto": area_texto,
        "rect": rect,
        "rect_sombra": rect_sombra,
        "ancho": 200,
        "alto": 40,
        "font": font
    }

def wrap_input(texto_dict: dict, font: Font) -> dict:
    data = crear_input(texto_dict["valor"], font)

    def render(area: pygame.Surface, pos: tuple[int, int], eventos: list[Event]) -> None:
        data["rect"].topleft = pos
        data["rect_sombra"].topleft = (pos[0], pos[1] + 4)

        fondo = (2, 18, 35)  # azul
        sombra = COLOR_LETRA_ACTIVO_SOMBRA  # amarillo
        borde_color = COLOR_LETRA_ACTIVO  # amarillo
        borde_width = 2

        pygame.draw.rect(area, sombra, data["rect_sombra"])

        pygame.draw.rect(area, fondo, data["rect"])

        pygame.draw.rect(area, borde_color, data["rect"], width=borde_width)

        area.blit(
            data["area_texto"],
            (
                data["rect"].centerx - data["area_texto"].get_width() // 2,
                data["rect"].centery - data["area_texto"].get_height() // 2,
            )
        )
    
    return {
        "render": render,
        "ancho": data["ancho"],
        "alto": data["alto"]
    }

def manejar_click_input(input: dict, eventos: list[pygame.event.Event]) -> None:
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if input["rect"].collidepoint(evento.pos):
                input["callback"]()