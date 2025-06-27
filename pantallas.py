import sys
from utils import cambiar_pantalla


pant_inicio = [
    { "tipo": "boton", "valor": "Jugar",        "pos": (370, 200), "callback": lambda: cambiar_pantalla("jugar") },
    { "tipo": "boton", "valor": "Estadísticas", "pos": (350, 260), "callback": lambda: cambiar_pantalla("estadisticas") },
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
    { "tipo": "boton",  "valor": "Volver",                  "pos": (690, 550), "callback": lambda: cambiar_pantalla("inicio") },
]

pant_creditos = [
    { "tipo": "texto",  "valor": "Créditos", "pos": (400, 45) },
    { "tipo": "texto",  "valor": "Juego hecho por: Bautista", "pos": (400, 125) },
    { "tipo": "boton",  "valor": "Volver",   "pos": (690, 550), "callback": lambda: cambiar_pantalla("inicio") },
]