import sys
from utils import cambiar_pantalla


pant_inicio = [
    { "tipo": "boton", "valor": "Jugar",        "pos": (400, 200), "callback": lambda: cambiar_pantalla("jugar") },
    { "tipo": "boton", "valor": "Estadísticas", "pos": (400, 260), "callback": lambda: cambiar_pantalla("estadisticas") },
    { "tipo": "boton", "valor": "Créditos",     "pos": (400, 320), "callback": lambda: cambiar_pantalla("creditos") },
    { "tipo": "boton", "valor": "Salir",        "pos": (400, 380), "callback": lambda: sys.exit(0) },
]

pant_jugar = [
    { "tipo": "texto",  "valor": "Nivel: 1",                "pos": (400, 80) },
    { "tipo": "texto",  "valor": "Puntos: 0",               "pos": (400, 120) },
    { "tipo": "boton",  "valor": "Palabras a completar",    "pos": (400, 200), "callback": lambda: print("palabras a completar") },
    { "tipo": "texto",  "valor": "Pista: Ejemplo de pista", "pos": (400, 260) },
    { "tipo": "boton",  "valor": "Volver",                  "pos": (400, 320), "callback": lambda: cambiar_pantalla("inicio") },
    { "tipo": "palabra",  "valor": "PESO",                  "pos": (450, 450), "callback": lambda: cambiar_pantalla("inicio") },
]

pant_estadisticas = [
    { "tipo": "texto",  "valor": "Estadísticas Generales", "pos": (400, 100) },
    { "tipo": "texto",  "valor": "Lista de jugadores",      "pos": (400, 160) },
    { "tipo": "boton",  "valor": "Volver",                  "pos": (400, 300), "callback": lambda: cambiar_pantalla("inicio") },
]

pant_creditos = [
    { "tipo": "texto",  "valor": "Créditos", "pos": (400, 100) },
    { "tipo": "texto",  "valor": "Juego hecho por: Bautista", "pos": (400, 160) },
    { "tipo": "boton",  "valor": "Volver",   "pos": (400, 300), "callback": lambda: cambiar_pantalla("inicio") },
]