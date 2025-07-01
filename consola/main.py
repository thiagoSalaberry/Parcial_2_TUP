from funcs import *

def main() -> None:
    eleccion = menu()

    opciones = [jugar, leer_estadisticas, creditos, salir]
    opciones[eleccion - 1]()
    

main()
