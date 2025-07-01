import os
import pygame
from consola.utils import negrita

RUTA_DATA = "data"
ARCH_NIVELES = os.path.join(RUTA_DATA, "niveles.json")
ARCH_ESTAD = os.path.join(RUTA_DATA, "estadisticas.txt")



# font = pygame.font.Font("assets/font.ttf", 24)
COLOR_TEXTO = (252, 255, 46)
COLOR_BOTON = (27, 36, 201)
COLOR_BOTON_SOMBRA = (181, 139, 0)



# font = pygame.font.Font("assets/font.ttf", 24)
color = (203, 219,  208)
COLOR_TEXTO = (2, 28, 40)
COLOR_TEXTO = (240, 238, 233)
COLOR_BOTON = (255, 209, 56)
COLOR_LETRA_CORRECTO=(255, 209, 56)
COLOR_LETRA_CORRECTO_SOMBRA=(181, 139, 0)
COLOR_LETRA_INCORRECTO=(255, 56, 56)
COLOR_LETRA_INCORRECTO_SOMBRA=(181, 0, 0)
COLOR_LETRA_ACTIVO=COLOR_LETRA_CORRECTO
COLOR_LETRA_ACTIVO_SOMBRA=COLOR_LETRA_CORRECTO_SOMBRA
COLOR_LETRA_DEFAULT=(212, 212, 212)
COLOR_LETRA_DEFAULT_SOMBRA=(93, 96, 100)

color_boton = (245, 206, 10)  # amarillo
color_texto= (9, 5, 250)
#texto = fuente.render("Jugar", True, color_texto)  # azul