import pygame
from pygame.font import Font
from pygame import Surface
from constantes import COLOR_TEXTO

def render_texto(area: Surface, texto_el: dict, font: Font = None) -> None:
        if font is None:
            font = pygame.font.SysFont(None, 24)
        
        x, y = texto_el["pos"]
        texto = font.render(texto_el["valor"], True, COLOR_TEXTO)
        area_texto = texto.get_rect(center=(x, y))

        area.blit(texto, area_texto)