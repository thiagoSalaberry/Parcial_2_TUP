from funciones import *
import json
import os
def main() -> None:
    completadas = []
    while len(completadas) < 8:
        datos_nivel = cargar_nivel("facil")
        palabras = datos_nivel["palabras"]
        pistas = datos_nivel["pistas"]
        mostrar_juego("facil", completadas)
        while True:
            i_palabra = input("Ingresá la palabra a cargar: ")
            if not i_palabra.isdigit():
                print("❌ Error: ingresá un número del 1 al 8")
                continue
            if int(i_palabra) not in range(1, 9):
                print("❌ Error: ingresá un número del 1 al 8")
                continue
            i_palabra = int(i_palabra)
            if i_palabra - 1 in completadas:
                print(f"⚠️ Error: la palabra {i_palabra} ya está completada, elegí otra")
                continue
            break


        print(f"Pista palabra {i_palabra}: {pistas[i_palabra - 1]}")
        palabra = input("Ingresá la palabra: ")
        if palabra.strip().upper() == palabras[i_palabra - 1]:
            os.system("cls")
            print("¡✅ La palabra es correcta!")
            completadas.append(i_palabra - 1)
        else:
            os.system("cls")
            print("❌ Esa no es la palabra, intentá de nuevo")
    mostrar_juego("facil", completadas)
    print(f"¡🥳 Felicitaciones, ganaste el nivel fácil!")
    salir()
    # datos_nivel = cargar_nivel("dificil")
    # print(json.dumps(datos_nivel, indent=4))
main()
