import os

# 📂📄 Carpetas y archivos
RUTA_DATA = "data"
ARCH_NIVELES = os.path.join(RUTA_DATA, "niveles.json")
ARCH_ESTAD = os.path.join(RUTA_DATA, "estadisticas.txt")
APP_PATH = os.path.dirname(os.path.realpath(__file__))
ASSETS_PATH = os.path.join(APP_PATH, "assets")

# 🔴🔵🟢🟡 Colores
COLOR_TEXTO = (252, 255, 46)
COLOR_BOTON = (27, 36, 201)
COLOR_BOTON_SOMBRA = (181, 139, 0)
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

# 🖥️ Pantallas
pant_estadisticas = [
    { "tipo": "texto",  "valor": "RANKING", "pos": (400, 45) },
]
pant_creditos = [
    { "tipo": "texto",  "valor": "CRÉDITOS", "pos": (400, 45) },
    { "tipo": "texto",  "valor": "Autores:", "pos": (400, 75) },
    { "tipo": "texto",  "valor": "  -   Bautista Ruiz", "pos": (400, 105) },
    { "tipo": "texto",  "valor": "  -   Thiago Salaberryz", "pos": (400, 125) },
    { "tipo": "texto",  "valor": "Fecha de Desarrollo:", "pos": (400, 165) },
    { "tipo": "texto",  "valor": "  -   Junio 2025", "pos": (400, 195) },
    { "tipo": "texto",  "valor": "Materia:", "pos": (400, 235) },
    { "tipo": "texto",  "valor": "  -   Programación I", "pos": (400, 265) },
    { "tipo": "texto",  "valor": "Docente:", "pos": (400, 305) },
    { "tipo": "texto",  "valor": "  -   Prof. Martín Alejandro García y Verónica Natalia Carbonari", "pos": (400, 335) },
    { "tipo": "texto",  "valor": "Carrera:", "pos": (400, 375) },
    { "tipo": "texto",  "valor": "  -   Tecnicatura Universitaria en Programación - UTN Avellaneda", "pos": (400, 405) },
    { "tipo": "texto",  "valor": "Emails de contacto:", "pos": (400, 445) },
    { "tipo": "texto",  "valor": "  -   bautyruiz1011@gmail.com", "pos": (400, 475) },
    { "tipo": "texto",  "valor": "  -   thiagosalaberry99@gmail.com", "pos": (400, 505) },
]