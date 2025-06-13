
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