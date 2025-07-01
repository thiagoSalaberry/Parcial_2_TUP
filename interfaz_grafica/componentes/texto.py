# import pygame
# from pygame.font import Font
# from pygame import Surface
# from consola.constantes import COLOR_TEXTO

# texto_el_modelo = {
#     "tipo": "texto",
#     "valor": "Texto de ejemplo",
#     "pos": (100, 100)
# }

# def texto(area: Surface, texto_el: dict, font: Font = None) -> None:
#     if font is None:
#         font = pygame.font.SysFont(None, 24)
    
#     x, y = texto_el["pos"]
#     texto = font.render(texto_el["valor"], True, COLOR_TEXTO)
#     area_texto = texto.get_rect(center=(x, y))

#     area.blit(texto, area_texto)

