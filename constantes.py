import os
import pygame
from utils import negrita

RUTA_DATA = "data"
ARCH_NIVELES = os.path.join(RUTA_DATA, "niveles.json")
ARCH_ESTAD = os.path.join(RUTA_DATA, "estadisticas.txt")

margen = 10

font = pygame.font.Font("assets/font.ttf", 24)

def sum(largo: int) -> int:
    return len(largo) + margen * 2 + 1 if (len(largo) + margen * 2) % 2 == 0 else len(largo) + margen * 2

MENU = f"""{"─" * sum("🎮 CODY CROSS")}
{" " * margen + negrita("🎮 CODY CROSS") + " " * margen}
{"─" * sum("🎮 CODY CROSS")}
Elegí una de las siguientes opciones:
1. Jugar 🕹️
2. Estadísticas 🏅
3. Créditos 🧑‍💻
4. Salir 🚪
"""

MENSAJE_DE_ESTADISTICAS = f"""{"─" * sum("🏅 Mejores 10 Jugadores 🏅")}
{" " * margen + negrita("🏅 Mejores 10 Jugadores 🏅") + " " * margen}
{"─" * sum("🏅 Mejores 10 Jugadores 🏅")}"""

MENSAJE_DE_CREDITOS = f"""{"─" * sum("Créditos")}
{" " * margen + negrita("Créditos") + " " * margen}
{"─" * sum("Créditos")}

Autores:
    ▫️ {negrita("Bautista Ruiz")}
    ▫️ {negrita("Thiago Salaberryz")}
Fecha de Desarrollo: {negrita("Junio 2025")}
Materia: {negrita("Programación I")}
Docente: {negrita("Prof. Martín Alejandro García y Verónica Natalia Carbonari")}
Carrera: {negrita("Tecnicatura Universitaria en Programación - UTN Avellaneda")}
Emails de contacto:
    ▫️ {negrita("bautyruiz1011@gmail.com")}
    ▫️ {negrita("thiagosalaberry99@gmail.com")}
"""


MENSAJE_DE_SALIDA = f"¡Gracias por jugar a {negrita("CODY CROSS")}!\n¡Hasta la próxima! 👋"


# font = pygame.font.Font("assets/font.ttf", 24)
color = (203, 219,  208)