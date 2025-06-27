eventos = {}

def on(evento: str, callback: callable) -> None:
    if evento not in eventos:
        eventos[evento] = []
    eventos[evento].append(callback)

def trigger(evento: str, *args, **kwargs) -> None:
    for cb in eventos.get(evento, []):
        cb(*args, **kwargs)
