estado = {
    "data": {
        "pantalla": "",
        "score": 0,
        "nivel_actual": "",
        "i_palabra_actual": 0,
        "palabra_actual": "",
        "palabras_completadas": [],
        "palabras": [],
        "acertadas": [],
        "palabras_validadas": [],
        "pistas": [],
    },
    "listeners": []
}


def get_estado(campo: str = None) -> dict:
    if campo:
        if campo not in estado["data"]:
            print(f"⚠️  El campo {campo} no pertenece al estado")
        return estado["data"][campo]
    return estado["data"]


def set_estado(nuevos_valores: dict) -> None:
    cambios = False
    for campo, valor in nuevos_valores.items():
        if campo not in estado["data"]:
            print(f"⚠️  El campo {campo} no pertenece al estado")
            continue
        if type(valor) is not type(estado["data"][campo]):
            print(f"⚠️  El tipo de dato de valor '{type(valor)}' es distinto al tipo del campo {campo} ({type(campo)})")
            continue
        if estado["data"][campo] != valor:
            estado["data"][campo] = valor
            cambios = True

    if cambios:
        for listener in estado["listeners"]:
            listener()


def subscribe(callback: callable) -> None:
    estado["listeners"].append(callback)

