estado = {
    "pantalla": "",
    "score": 0,
    "nivel_actual": "",
    "i_palabra_actual": 0,
    "palabra_actual": "",
    "palabras_completadas": [],
    "palabras": [],
    "palabras_validadas": [],
    "pistas": [],
    "listeners": []
}

def set_estado(nuevos_valores: dict) -> dict:
    for campo, valor in nuevos_valores.items():
        if campo not in estado:
            print(f"⚠️  El campo {campo} no pertenece al estado")
            continue
        if type(valor) is not type(estado[campo]):
            print(f"⚠️  El tipo de dato de valor '{type(valor)}' es distinto al tipo del campo {campo} ({type(campo)})")
            continue
        estado[campo] = valor
    for listener in estado["listeners"]:
        listener()

    return estado

def subscribe(callback: callable) -> None:
    estado["listeners"].append(callback)
