import pygame
import sys

def play():
    pygame.init()

    ancho = 800
    alto = 600
    color = (203, 219,  208)

    pantalla = pygame.display.set_mode((ancho, alto))

    pygame.display.set_caption("CODY CROSS")
    clock = pygame.time.Clock()
    ejecutando = True

    font = pygame.font.Font("assets/font.ttf", 24)
    fondo = pygame.image.load("assets/fondo.png").convert()
    fondo = pygame.transform.scale(fondo, pantalla.get_size())

    # def texto(texto: str, size: int) -> pygame.Surface:
    #     font = pygame.font.Font("assets/font.ttf", size)
    #     color = (0, 0, 0)  # Negro
    #     superficie = font.render(texto, True, color)
    #     return superficie

    def boton(texto: str, x: int, y: int, ancho_fijo: int, cb: callable) -> dict:
        padding = 10
        area_texto = font.render(texto, True, (0,0,0))
        rect_texto = area_texto.get_rect()

        alto = rect_texto.height + padding * 2
        boton_rect = pygame.Rect(
            x, y,
            ancho_fijo,
            alto
        )

        # 🧱 Sombra (como box-shadow: 0 4px 0 0 color)
        sombra_color = (165, 176, 168)  # Elegí un gris oscuro
        sombra_rect = boton_rect.copy()
        sombra_rect.y += 4
        pygame.draw.rect(pantalla, sombra_color, sombra_rect, border_radius=5)

        texto_x = x + (ancho_fijo - rect_texto.width) // 2
        texto_y = y + padding

        pygame.draw.rect(pantalla, color, boton_rect, border_radius=5)
        pantalla.blit(area_texto, (texto_x, texto_y))

        return {
            "rect": boton_rect,
            "cb": cb
        }


    while ejecutando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in botones_renderizados:
                    if btn["rect"].collidepoint(event.pos):
                        btn["cb"]()
        pantalla.blit(fondo, (0, 0))

        # pantalla.fill((255, 255, 255))
        
        # titulo = texto("CODY CROSS", 64)
        # pantalla.blit(titulo, (100, 50))

        padding = 20
        gap = 60
        botones = [
            ("Jugar", lambda: print("¡A jugar!")),
            ("Estadísticas", lambda: print("Ver estadísticas")),
            ("Créditos", lambda: print("Ver créditos")),
            ("Salir", lambda: sys.exit(0))
        ]
        anchos = [
            font.render(txt, True, (0,0,0)).get_width() + padding * 2
            for txt, _ in botones
        ]
        ancho_max = max(anchos)

        botones_renderizados = []
        for i, (texto, cb) in enumerate(botones):
            x = (pantalla.get_width() - ancho_max) // 2            
            y = gap * i + 100
            boton_info = boton(texto, x, y, ancho_max, cb)
            botones_renderizados.append(boton_info)
        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)

play()
        
