estado = {
    "pantalla": "inicio",
    "score": 0,
    "nivel_actual": "facil",
    "i_palabra_actual": 0,
    "palabra_actual": "",
    "palabras_completadas": [
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ],
    "palabras": [],
    "pistas": [],
}

def set_estado(campo: str, valor: any) -> dict:
    if campo not in estado.keys():
        print(f"⚠️  El campo {campo} no pertenece al estado")
        return estado
    if type(valor) is not type(estado[campo]):
        print(f"⚠️  El tipo de dato de valor '{type(valor)}' es distinto al tipo del campo {campo} ({type(campo)})")
        return estado
    estado[campo] = valor
    return estado
