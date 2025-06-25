from estado import set_estado

def negrita(texto: str) -> str:
    return f"\033[1m{texto}\033[0m"

def cambiar_pantalla(pantalla: str) -> None:
    if pantalla not in ["inicio", "jugar", "estadisticas", "creditos"]:
        raise ValueError("'pantalla' debe ser 'inicio', 'jugar', 'estadisticas' o 'creditos'.")

    set_estado("pantalla", pantalla)