import pygame
from pygame import Surface
from pygame.font import Font
from pygame.event import Event
from componentes.boton import manejar_click_boton, crear_boton
from componentes.input import manejar_click_input
from consola.constantes import COLOR_BOTON, COLOR_BOTON_SOMBRA, COLOR_TEXTO, COLOR_LETRA_CORRECTO_SOMBRA, COLOR_LETRA_ACTIVO, COLOR_LETRA_ACTIVO_SOMBRA, COLOR_LETRA_CORRECTO, COLOR_LETRA_DEFAULT, COLOR_LETRA_DEFAULT_SOMBRA, COLOR_LETRA_INCORRECTO, COLOR_LETRA_INCORRECTO_SOMBRA

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

    area_texto = font.render(texto, True, (0, 0, 0))
    rect_texto = area_texto.get_rect()

    if tipo_ancho == "auto":
        ancho = rect_texto.width + padding_x * 2
    else:
        ancho = ancho_fijo

    alto = rect_texto.height + padding_y * 2

    rect = pygame.Rect(x, y, ancho, alto)
    sombra_rect = pygame.Rect(x, y + 4, ancho, alto)

    return {
        "texto": texto,
        "ancho": ancho,
        "alto": alto,
        "rect": rect,
        "sombra_rect": sombra_rect,
        "callback": callback,
        "area_texto": area_texto,
        "font": font
    }


def manejar_click_boton(boton: dict, eventos: list[pygame.event.Event]) -> None:
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton["rect"].collidepoint(evento.pos):
                boton["callback"]()


def boton(area: Surface, boton: dict, eventos: list[pygame.event.Event], font: Font) -> None:
    boton = crear_boton(boton["pos"][0], boton["pos"][1], boton["valor"], boton["callback"], font=font)
    rect: pygame.Rect = boton["rect"]
    sombra_rect: pygame.Rect = boton["sombra_rect"]
    pygame.draw.rect(area, COLOR_BOTON_SOMBRA, sombra_rect, border_radius=5)
    pygame.draw.rect(area, COLOR_BOTON, rect, border_radius=5)
    area.blit(
        boton["area_texto"],
        (
            rect.centerx - boton["area_texto"].get_width() // 2,
            rect.centery - boton["area_texto"].get_height() // 2
        )
    )
    manejar_click_boton(boton, eventos)

def wrap_boton(boton_dict: dict, font: Font) -> dict:
    data = crear_boton(0, 0, boton_dict["valor"], boton_dict["callback"], font=font)

    def render(area: pygame.Surface, pos: tuple[int, int], eventos: list[Event]) -> None:
        data["rect"].topleft = pos
        data["sombra_rect"].topleft = (pos[0], pos[1] + 4)
        pygame.draw.rect(area, COLOR_BOTON_SOMBRA, data["sombra_rect"], border_radius=5)
        pygame.draw.rect(area, COLOR_BOTON, data["rect"], border_radius=5)

        area.blit(
            data["area_texto"],
            (
                data["rect"].centerx - data["area_texto"].get_width() // 2,
                data["rect"].centery - data["area_texto"].get_height() // 2,
            )
        )
        manejar_click_boton(data, eventos)

    return {
        "render": render,
        "ancho": data["ancho"],
        "alto": data["alto"]
    }




