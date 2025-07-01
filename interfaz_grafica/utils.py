"""
Este módulo se encarga de la lógica de lectura y escritura de los archivos
"""
import json
from constantes import ARCH_NIVELES, ARCH_ESTAD
from estado import get_estado, set_estado


def leer_niveles(arch_niveles: str = ARCH_NIVELES) -> dict:
    """
    Lee el archivo de los datos de los niveles.
    Args:
        arch_niveles (str): Nombre del archivo
    Returns:
        dict: Datos de los niveles
    """
    with open(arch_niveles, "r", encoding="utf-8") as archivo_niveles:
        datos_niveles = json.load(archivo_niveles)
    
    return datos_niveles["niveles"]


def leer_estadisticas(arch_estad: str = ARCH_ESTAD) -> list[str]:
    """
    Lee el archivo de las estadísticas de los jugadores
    Args:
        arch_estad (str): Ruta al archivo de estadísticas
    Returns:
        estadisticas (list[str]): Lista de cada uno de los registros
    """
    with open(arch_estad, "r") as file:
        lineas = file.readlines()

    estadisticas = [linea.replace("\n", "") for linea in lineas]

    return estadisticas


def cargar_estadisticas(arch_estad: str = ARCH_ESTAD) -> None:
    """
    Actualiza el archivo de estadísticas y reinicia el estado.
    Args:
        arch_estad (str): Ruta al archivo de estadísticas
    """
    score = get_estado("score")
    estadisticas = leer_estadisticas()
    puntajes = [int(linea.split(" - ")[1]) for linea in estadisticas]
    nombre_jugador = get_estado("nombre_jugador")

    data_niveles = leer_niveles()

    if not nombre_jugador:
        return

    if not puntajes or len(puntajes) < 10 or (len(puntajes) == 10 and score > puntajes[-1]):
        estadisticas: list[str] = leer_estadisticas()

        estadisticas.append(f"{nombre_jugador} - {score}")
        estadisticas.sort(key=lambda x: int(x.split(" - ")[1]), reverse=True)

        with open(arch_estad, "w") as file:
            file.writelines([f"{linea}\n" for linea in estadisticas][:10])

    estado_inical = {
        "pantalla": "estadisticas",
        "nivel_actual": "facil",
        "estado_nivel_actual": "jugando",
        "palabras": data_niveles["facil"]["palabras"],
        "palabras_validadas": [False] * 8,
        "palabras_completadas": [""] * 8,
        "acertadas": [False] * 8,
        "pistas": data_niveles["facil"]["pistas"],
        "score": 0,
        "i_palabra_actual": 0,
        "palabra_actual": "",
        "juego_ganado": False,
        "nombre_jugador": ""
    }
    set_estado(estado_inical)