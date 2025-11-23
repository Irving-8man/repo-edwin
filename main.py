# main.py
"""
Simulador de Autómatas y Gramáticas
Este programa permite simular diferentes modelos de computación:
-> AFD: Autómata Finito Determinista
-> GRAMATICA_REGULAR: Gramáticas Regulares
-> GLC: Gramáticas Libres de Contexto
-> AP: Autómata de Pila
-> MT: Máquina de Turing

USO:
1. Coloca archivos JSON en la carpeta ejemplos
2. Ejecuta este script
3. Selecciona el archivo a procesar
"""

import json
import os
from modos.afd import ModoAFD
from modos.gramatica_regular import ModoGramaticaRegular
from modos.glc import ModoGLC
from modos.ap import ModoAP
from modos.mt import ModoMT


"""
Carga y ejecuta un archivo JSON con la configuración del autómata

Args:
nombre_archivo: Nombre del archivo JSON en la carpeta "ejemplos"
"""
def ejecutar_archivo(nombre_archivo):
    ruta = os.path.join("ejemplos", nombre_archivo)
    
    # Verificar que el archivo existe
    if not os.path.isfile(ruta):
        print(f"El archivo '{nombre_archivo}' no existe en la carpeta 'ejemplos/'.")
        return
    
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            data = json.load(archivo)
    except json.JSONDecodeError as e:
        print(f"Error al leer el JSON: {e}")
        return
    except Exception as e:
        print(f"Error inesperado: {e}")
        return
    
    # Identificando el modo de
    modo = data.get("modo", "").upper()
    
    # Seleccion del modo y pasando la data del JSON
    if modo == "AFD":
        simulador = ModoAFD(data)
    elif modo == "GRAMATICA_REGULAR":
        simulador = ModoGramaticaRegular(data)
    elif modo == "GLC":
        simulador = ModoGLC(data)
    elif modo == "AP":
        simulador = ModoAP(data)
    elif modo == "MT":
        simulador = ModoMT(data)
    else:
        print(f"Modo '{modo}' no reconocido. Modos válidos: AFD, GRAMATICA_REGULAR, GLC, AP, MT")
        return
    
    # Ejecutar la simulación
    print("\n")
    print(f"Ejecutando modo: {modo}")
    simulador.ejecutar()




def main():

    while True:
        print("\n")
        print("=== SIMULADOR DE MODELOS DE COMPUTACIÓN ===")
        
        # Comprobando que existe la carpeta ejemplos
        if not os.path.exists("ejemplos"):
            print("No existe la carpeta 'ejemplos/'. Créala y añade archivos JSON.")
            break
        
        # Mostrando los JSON disponibles
        archivos = [f for f in os.listdir("ejemplos") if f.endswith(".json")]
        
        if not archivos:
            print("No hay archivos JSON en la carpeta ejemplos")
            break
        
        print("\nArchivos disponibles:")
        for i, archivo in enumerate(archivos, 1):
            print(f"  {i}. {archivo}")
        
        nombre_archivo = input("\nIngrese el nombre del archivo JSON: ").strip()
        
        # Permitir que seleccione un modo
        if nombre_archivo.isdigit():
            idx = int(nombre_archivo) - 1
            if 0 <= idx < len(archivos):
                nombre_archivo = archivos[idx]
            else:
                print("Número inválido.")
                continue
        
        # Ejecutando el archivo
        ejecutar_archivo(nombre_archivo)


        print("\n")
        print("¿Desea procesar otro archivo?")
        print("1. Sí")
        print("2. No (salir)")
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion != "1":
            print("\nSaliendo del simulador...")
            break



#Ejecution principal para evitar problemas
if __name__ == "__main__":
    main()