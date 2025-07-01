import pygame
from pygame import Surface
from pygame.font import Font
from pygame.event import Event
from constantes import COLOR_BOTON, COLOR_BOTON_SOMBRA

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
    """
    Crea el diccionario de un botón listo para renderizar
    Args:
        x (int): Posición en X
        y (int): Posición en Y
        texto (str): Texto del botón
        callback (callable): Función a ejecutar al hacer click
        tipo_ancho (str): Define si el botón tiene que tomar el ancho propio (texto + padding_x * 2) o tomar el ancho del contenedor
        padding_x (int): Distancia entre el texto y los márgenes verticales del botón
        padding_y (int): Distancia entre el texto y los márgenes horizontales del botón
    Returns:
        dict: Datos del botón listos para renderizar
    """
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
    """
    Recibe los eventos y si el click es dentro del área del botón, ejecuta su callback
    Args:
        boton (dict): Datos del botón
        eventos (list[pygame.event.Event]): Lista de los eventos de pygame
    """
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton["rect"].collidepoint(evento.pos):
                boton["callback"]()


def boton(area: Surface, boton: dict, eventos: list[pygame.event.Event], font: Font) -> None:
    """
    Crea y renderiza un botón sobre la pantalla
    Args:
        area (Surface): Superficie de pygame sobre la cual renderizar el botón
        boton (dict): Datos del botón
        eventos (list[pygame.event.Event]): Lista de los eventos de pygame
    """
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
    """
    A diferencia de boton() que renderiza un único botón individual, esta función se encarga 
    de estandarizar un botón y dejarlo listo para pasarlo a una función que se encargue de renderizar
    varios elementos de diferentes tipos y pueda manejar los anchos, altos, separaciones entre elementos
    y cómo renderizar cada uno. Existe una función wrap para cada uno de los elementos.
    Args:
        boton_dict (dict): Datos del botón
        font (Font): Fuente con la cual escribir los textos
    Returns:
        render (callable): Forma de renderizar el botón
        ancho (int): Ancho del botón
        alto (int): Alto del botón
    """
    data = crear_boton(0, 0, boton_dict["valor"], boton_dict["callback"], font=font)

    def render(area: pygame.Surface, pos: tuple[int, int], eventos: list[Event]) -> None:
        """
        Este función de render se define dentro de la función de wrap porque solo sirve para renderizar
        este tipo de elementos. Cada función wrap definirá su propia función render que a su vez definirá
        cómo renderizar cada elemento en particular
        Args:
            area (pygame.Surface): Superficie de pygame sobre la cual renderizar el botón
            pos (tuple[int, int]): Posición del elemento
            eventos (list[Event]): Lista de los eventos de pygame
        
        """
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




