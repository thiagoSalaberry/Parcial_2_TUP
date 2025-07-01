import sys
from interfaz_grafica.utils_pygame import cambiar_pantalla

pant_inicio = [
    { "tipo": "boton", "valor": "Jugar",        "pos": (180, 520), "callback": lambda: cambiar_pantalla("jugar") },
    { "tipo": "boton", "valor": "Estadísticas", "pos": (280, 520), "callback": lambda: cambiar_pantalla("estadisticas") },
    { "tipo": "boton", "valor": "Créditos",     "pos": (430, 520), "callback": lambda: cambiar_pantalla("creditos") },
    { "tipo": "boton", "valor": "Salir",        "pos": (550, 520), "callback": lambda: sys.exit(0) },
]


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