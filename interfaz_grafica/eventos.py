eventos = {}

def on(evento: str, callback: callable) -> None:
    """
    Agrega y ejecuta eventos cuando sean invocados.
    Args:
        evento (str): Nombre mediante el cual se invocará el evento 
        callback (callable): Función a ejecutar en la invocación
    Returns:
        None
    """
    if evento not in eventos:
        eventos[evento] = []
    eventos[evento].append(callback)

def trigger(evento: str, *args, **kwargs) -> None:
    """
    Invoca al evento mediante su nombre con los argumentos posicionales y argumentos de nombre pasados.
    Args:
        evento (str): Nombre del evento a invocar
        *args: Argumentos posicionales
        **kwargs: Argumentos de clave valor
    Returns:
        None
    """
    for cb in eventos.get(evento, []):
        cb(*args, **kwargs)
