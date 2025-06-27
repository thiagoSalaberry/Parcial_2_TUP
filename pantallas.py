import sys
from utils import cambiar_pantalla


pant_inicio = [
    { "tipo": "boton", "valor": "Jugar",        "pos": (370, 200), "callback": lambda: cambiar_pantalla("jugar") },
    { "tipo": "boton", "valor": "Estadísticas", "pos": (345, 260), "callback": lambda: cambiar_pantalla("estadisticas") },
    { "tipo": "boton", "valor": "Créditos",     "pos": (360, 320), "callback": lambda: cambiar_pantalla("creditos") },
    { "tipo": "boton", "valor": "Salir",        "pos": (375, 380), "callback": lambda: sys.exit(0) },
]

pant_jugar = [
    { "tipo": "texto",  "valor": "Nivel: 1",                "pos": (55, 30) },
    { "tipo": "texto",  "valor": "Puntos: 0",               "pos": (60, 50) },
    { "tipo": "texto",  "valor": "Pista: Ejemplo de pista", "pos": (400, 530) },
    { "tipo": "boton",  "valor": "Volver",                  "pos": (690, 550), "callback": lambda: cambiar_pantalla("inicio") },
    { "tipo": "palabra",  "valor": "PESO",                  "pos": (450, 450), "callback": lambda: cambiar_pantalla("inicio") },
]

pant_estadisticas = [
    { "tipo": "texto",  "valor": "Ranking", "pos": (400, 45) },
    { "tipo": "texto",  "valor": "1 - Mateo", "pos": (400, 85) },
    { "tipo": "texto",  "valor": "2 - Valentina", "pos": (400, 125) },
    { "tipo": "texto",  "valor": "3 - Thiago", "pos": (400, 165) },
    { "tipo": "texto",  "valor": "4 - Isabella", "pos": (400, 205) },
    { "tipo": "texto",  "valor": "5 - Benjamín", "pos": (400, 245) },
    { "tipo": "texto",  "valor": "6 - Sofía", "pos": (400, 285) },
    { "tipo": "texto",  "valor": "7 - Santiago", "pos": (400, 325) },
    { "tipo": "texto",  "valor": "8 - Emma", "pos": (400, 365) },
    { "tipo": "texto",  "valor": "9 - Joaquín", "pos": (400, 405) },
    { "tipo": "texto",  "valor": "10 - Olivia", "pos": (400, 445) },
    { "tipo": "boton",  "valor": "Volver",                  "pos": (690, 550), "callback": lambda: cambiar_pantalla("inicio") },
]

pant_creditos = [
    { "tipo": "texto",  "valor": "Créditos", "pos": (400, 45) },
    { "tipo": "texto",  "valor": "Autores:", "pos": (400, 75) },
    { "tipo": "texto",  "valor": "Bautista Ruiz", "pos": (400, 105) },
    { "tipo": "texto",  "valor": "Thiago Salaberryz", "pos": (400, 125) },
    { "tipo": "texto",  "valor": "Fecha de Desarrollo:", "pos": (400, 165) },
    { "tipo": "texto",  "valor": "Junio 2025", "pos": (400, 195) },
    { "tipo": "texto",  "valor": "Materia:", "pos": (400, 235) },
    { "tipo": "texto",  "valor": "Programación I", "pos": (400, 265) },
    { "tipo": "texto",  "valor": "Docente:", "pos": (400, 305) },
    { "tipo": "texto",  "valor": "Prof. Martín Alejandro García y Verónica Natalia Carbonari", "pos": (400, 335) },
    { "tipo": "texto",  "valor": "Carrera:", "pos": (400, 375) },
    { "tipo": "texto",  "valor": "Tecnicatura Universitaria en Programación - UTN Avellaneda", "pos": (400, 405) },
    { "tipo": "texto",  "valor": "Emails de contacto:", "pos": (400, 445) },
    { "tipo": "texto",  "valor": "bautyruiz1011@gmail.com", "pos": (400, 475) },
    { "tipo": "texto",  "valor": "thiagosalaberry99@gmail.com", "pos": (400, 505) },
    { "tipo": "boton",  "valor": "Volver",   "pos": (690, 550), "callback": lambda: cambiar_pantalla("inicio") },
]