import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Mi pygame")

color_botones = (203, 219, 208)
fondo = (245, 245, 245)
fuente = pygame.font.SysFont("Arial", 30)

def draw_button(texto: str, x: int, y: int) -> pygame.Rect:
    ancho = 100
    alto = 44
    rect = pygame.Rect(x, y, ancho, alto)

    pygame.draw.rect(surface=SCREEN, color=color_botones, rect=rect)

    text_surf = fuente.render(texto, True, (0,0,0))
    text_rect = text_surf.get_rect(center=rect.center)
    SCREEN.blit(text_surf, text_rect)

    return rect


running = True
while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

    botones = ["Jugar", "Estadísticas", "Créditos", "Salir"]

    for i, boton in enumerate(botones):
        draw_button(boton, (SCREEN_WIDTH / 2 - 100 / 2), i * 50 + 50)
    pygame.display.flip()

pygame.quit()