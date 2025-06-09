from funciones import *
import json
import os
def main() -> None:
    niveles = ["facil", "intermedio", "dificil"]
    nivel_actual = 2
    puntos = 0
    while nivel_actual < len(niveles):
        nivel_actual, puntos = jugar_nivel(nivel_actual, niveles[nivel_actual], puntos=puntos)
    print("¡🎉 Felicitaciones, ganaste el juego!")
    cargar_estadisticas(puntos=puntos)
    salir()
    # datos_nivel = cargar_nivel("dificil")
    # print(json.dumps(datos_nivel, indent=4))
main()
