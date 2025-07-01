import pygame
from consola.constantes import COLOR_LETRA_CORRECTO
def wrap_recuadro(
    elementos: list[dict],
    padding: tuple[int, int] = (40, 20),
    gap: int = 20,
    direccion: str = "vertical",  # o "horizontal"
    jusfify: str = "center",
    font: pygame.font.Font = None
) -> dict:
    padding_x, padding_y = padding

    # Calculamos dimensiones internas del contenido
    if direccion == "vertical":
        ancho_contenido = max(e["ancho"] for e in elementos)
        alto_contenido = sum(e["alto"] for e in elementos) + gap * (len(elementos) - 1)
    else:
        ancho_contenido = sum(e["ancho"] for e in elementos) + gap * (len(elementos) - 1)
        alto_contenido = max(e["alto"] for e in elementos)

    ancho_total = ancho_contenido + padding_x * 2
    alto_total = alto_contenido + padding_y * 2

    rect = pygame.Rect(0, 0, ancho_total, alto_total)
    sombra_rect = pygame.Rect(0, 4, ancho_total, alto_total)

    def render(area: pygame.Surface, pos: tuple[int, int], eventos: list[pygame.event.Event]) -> None:
        rect.topleft = pos
        sombra_rect.topleft = (pos[0], pos[1] + 4)

        # Dibujar sombra
        # pygame.draw.rect(area, COLOR_LETRA_CORRECTO_SOMBRA, sombra_rect)

        # Dibujar fondo del recuadro
        # pygame.draw.rect(area, (2, 18, 35), rect)  # Azul oscuro
        rect_transparente = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(rect_transparente, (2, 18, 35, 128), rect_transparente.get_rect(), border_radius=10)
        area.blit(rect_transparente, rect.topleft)

        # Dibujar borde
        pygame.draw.rect(area, COLOR_LETRA_CORRECTO, rect, width=2)  # Amarillo

        # Renderizar los elementos dentro, centrados
        if direccion == "vertical":
            y = rect.top + padding_y
            for elem in elementos:
                if jusfify == "center":
                    x = rect.left + (ancho_total - elem["ancho"]) // 2
                elif jusfify == "left":
                    x = rect.left + padding_x
                elif jusfify == "right":
                    x = rect.left + ancho_total - elem["ancho"] - padding_x
                elem["render"](area, (x, y), eventos)
                y += elem["alto"] + gap
        else:
            x = rect.left + padding_x
            for elem in elementos:
                y = rect.top + (alto_total - elem["alto"]) // 2
                elem["render"](area, (x, y), eventos)
                x += elem["ancho"] + gap

    return {
        "render": render,
        "ancho": ancho_total,
        "alto": alto_total
    }
