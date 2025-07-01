import json
from constantes import ARCH_NIVELES


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