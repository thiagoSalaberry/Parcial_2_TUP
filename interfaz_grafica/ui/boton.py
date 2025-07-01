import pygame
from pygame.font import Font
from pygame.event import Event
from componentes.boton import manejar_click_boton, crear_boton
from componentes.input import manejar_click_input
from constantes import COLOR_BOTON, COLOR_BOTON_SOMBRA, COLOR_TEXTO, COLOR_LETRA_CORRECTO_SOMBRA, COLOR_LETRA_ACTIVO, COLOR_LETRA_ACTIVO_SOMBRA, COLOR_LETRA_CORRECTO, COLOR_LETRA_DEFAULT, COLOR_LETRA_DEFAULT_SOMBRA, COLOR_LETRA_INCORRECTO, COLOR_LETRA_INCORRECTO_SOMBRA
from interfaz_grafica.utils_pygame import grupo
# def crear_boton(x: int, y: int, texto: str, callback: callable, font: Font) -> dict:
#     pass

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

def crear_letra(letra: str, activo: bool, estado_palabra: str, estado_letra: str, i: int, callback: callable, font: Font) -> dict:
    if font is None:
        font = pygame.font.SysFont(None, 24)
    
    area_letra = font.render(letra, True, (40, 40, 40))
    rect = pygame.Rect(0, 0, 40, 40)
    rect_sombra = pygame.Rect(0, 4, 40, 40)

    return {
        "letra": letra,
        "activo": activo,
        "estado_palabra": estado_palabra,
        "estado_letra": estado_letra,
        "i": i,
        "callback": callback,
        "area_letra": area_letra,
        "rect": rect,
        "rect_sombra": rect_sombra,
        "ancho": 40,
        "alto": 40,
        "font": font
    }

def wrap_letra(letra_dict: dict, font: Font) -> dict:
    data = crear_letra(
        letra_dict["valor"],
        letra_dict["activo"],
        letra_dict["estado_palabra"],
        letra_dict["estado_letra"],
        letra_dict["i"],
        letra_dict["callback"],
        font
    )

    def render(area: pygame.Surface, pos: tuple[int, int], eventos: list[pygame.event.Event]) -> None:
        data["rect"].topleft = pos
        data["rect_sombra"].topleft = (pos[0], pos[1] + 4)

        # Colores según estado
        if data["estado_palabra"] == "bien":
            fondo = COLOR_LETRA_CORRECTO
            sombra = COLOR_LETRA_CORRECTO_SOMBRA
            borde_color = None
            borde_width = 0
        elif data["estado_palabra"] == "mal":
            fondo = COLOR_LETRA_INCORRECTO
            sombra = COLOR_LETRA_INCORRECTO_SOMBRA
            borde_color = None
            borde_width = 0
        elif data["letra"]:
            fondo = COLOR_LETRA_CORRECTO
            sombra = COLOR_LETRA_CORRECTO_SOMBRA
            borde_color = None
            borde_width = None
        elif data["activo"]:
            fondo = (2, 18, 35)  # azul
            sombra = COLOR_LETRA_ACTIVO_SOMBRA  # amarillo
            borde_color = COLOR_LETRA_ACTIVO  # amarillo
            borde_width = 2
        else:
            fondo = (2, 18, 35)  # azul
            sombra = (124, 124, 124)  # sombra gris más oscura
            borde_color = (212, 212, 212)  # borde gris
            borde_width = 2

        # Dibujar sombra
        pygame.draw.rect(area, sombra, data["rect_sombra"], border_radius=5)

        # Dibujar fondo
        pygame.draw.rect(area, fondo, data["rect"], border_radius=5)

        # Dibujar borde si corresponde
        if borde_color and borde_width > 0:
            pygame.draw.rect(area, borde_color, data["rect"], border_radius=5, width=borde_width)

        # Dibujar letra centrada
        area.blit(
            data["area_letra"],
            (
                data["rect"].centerx - data["area_letra"].get_width() // 2,
                data["rect"].centery - data["area_letra"].get_height() // 2,
            )
        )
        manejar_click_input(data, eventos)


    return {
        "render": render,
        "ancho": data["ancho"],
        "alto": data["alto"]
    }


def crear_palabra(
    correcta: str,
    ingresada: str,
    i: int,
    i_palabra_actual: str,
    callback: callable,
    font: Font
) -> list[dict]:
    letras = []
    estado_palabra = "bien" if ingresada == correcta and len(ingresada) == len(correcta) else "mal"

    for j, letra_correcta in enumerate(correcta):
        letra_ingresada = ingresada[j] if j < len(ingresada) else ""
        activo = i_palabra_actual == i # and j == len(ingresada)

        if letra_ingresada and letra_ingresada == letra_correcta:
            estado_letra = "bien"
        elif letra_ingresada:
            estado_letra = "mal"
        else:
            estado_letra = "default"
        
        letras.append(wrap_letra({
            "valor": letra_ingresada,
            "activo": activo,
            "estado_palabra": estado_palabra if len(ingresada) == len(correcta) else "default",
            "estado_letra": estado_letra,
            "i": j,
            "callback": callback
        }, font))

    letras.insert(0, wrap_texto({"valor": f"{i + 1}."}, font))
    return letras

def wrap_palabra(
    correcta: str,
    ingresada: str,
    i: int,
    i_palabra_actual: int,
    callback: callable,
    font: Font
) -> dict:
    letras = crear_palabra(correcta, ingresada, i, i_palabra_actual, callback, font)

    def render(area: pygame.Surface, pos: tuple[int, int], eventos: list[Event]) -> None:
        grupo(letras, "horizontal", 10, pos, area, eventos)
    
    ancho_total = sum(l["ancho"] for l in letras) + 10 * (len(letras) - 1)
    alto = max(l["alto"] for l in letras)

    return {
        "render": render,
        "ancho": ancho_total,
        "alto": alto
    }