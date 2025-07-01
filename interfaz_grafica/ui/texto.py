import pygame
from pygame import Surface
from pygame.font import Font
from pygame.event import Event
from consola.constantes import COLOR_TEXTO

def texto(area: Surface, texto_el: dict, font: Font = None) -> None:
    if font is None:
        font = pygame.font.SysFont(None, 24)
    
    x, y = texto_el["pos"]
    texto = font.render(texto_el["valor"], True, COLOR_TEXTO)
    area_texto = texto.get_rect(center=(x, y))

    area.blit(texto, area_texto)


def crear_texto(texto: str, font: Font) -> dict:
    if font is None:
        font = pygame.font.SysFont(None, 24)
    
    area = font.render(texto, True, COLOR_TEXTO)
    rect = area.get_rect()

    return {
        "texto": texto,
        "area": area,
        "ancho": rect.width,
        "alto": rect.height,
        "font": font
    }
    

def wrap_texto(texto_dict: dict, font: Font) -> dict:
    data = crear_texto(texto_dict["valor"], font)

    def render(area: pygame.Surface, pos: tuple[int, int], eventos: list[Event]) -> None:
        area.blit(data["area"], pos)

    return {
        "render": render,
        "ancho": data["ancho"],
        "alto": data["alto"]
    }