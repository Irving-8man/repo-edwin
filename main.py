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
3. Selecciona la configuración
4. Ingresa la cadena a validar
"""

import json
import os
from modos.afd import ModoAFD
from modos.glc import ModoGLC
from modos.gramatica_regular import ModoGramaticaRegular
from modos.ap import ModoAP
from modos.mt import ModoMT

def ejecutar_archivo(nombre_archivo):
    ruta = os.path.join("ejemplos", nombre_archivo)
    
    # Verificar que el archivo existe
    if not os.path.isfile(ruta):
        print(f"❌ El archivo '{nombre_archivo}' no existe en la carpeta 'ejemplos/'.")
        return False
    
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            data = json.load(archivo)
    except json.JSONDecodeError as e:
        print(f"❌ Error al leer el JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
    
    # Identificar el modo
    modo = data.get("modo", "").upper()
    print(f"\n{'='*50}")
    print(f"Modo: {modo}")
    print(f"Configuración: {nombre_archivo}")
    print(f"{'='*50}")
    
    # Bucle para procesar múltiples entradas con la misma configuración
    while True:
        print("\n")
        entrada = input("Ingresa la cadena a validar (o 'salir' para cambiar configuración): ").strip()
        
        if entrada.lower() == 'salir':
            return True
        
        # Agregar la entrada al diccionario de datos
        data["entrada"] = entrada
        
        # Selección del modo y creación del simulador
        if modo == "AFD":
            simulador = ModoAFD(data)
        elif modo == "GLC":
            simulador = ModoGLC(data)
        elif modo == "GRAMATICA_REGULAR":
            simulador = ModoGramaticaRegular(data)
        elif modo == "AP":
            simulador = ModoAP(data)
        elif modo == "MT":
            simulador = ModoMT(data)
        else:
            print(f"❌ Modo '{modo}' no reconocido. Modos válidos: AFD, GLC, GRAMATICA_REGULAR, AP, MT")
            return False
        
        # Ejecutar la simulación
        try:
            simulador.ejecutar()
        except Exception as e:
            print(f"❌ Error durante la simulación: {e}")
        
        print("\n" + "-"*50)

def main():
    print("\n")
    print("╔════════════════════════════════════════════════╗")
    print("║  SIMULADOR DE MODELOS DE COMPUTACIÓN          ║")
    print("╚════════════════════════════════════════════════╝")
    
    # Comprobar que existe la carpeta ejemplos
    if not os.path.exists("ejemplos"):
        print("\n❌ No existe la carpeta 'ejemplos/'. Créala y añade archivos JSON.")
        return
    
    while True:
        # Mostrar los JSON disponibles
        archivos = [f for f in os.listdir("ejemplos") if f.endswith(".json")]
        
        if not archivos:
            print("\n❌ No hay archivos JSON en la carpeta 'ejemplos/'")
            break
        
        print("\n📁 Configuraciones disponibles:")
        for i, archivo in enumerate(archivos, 1):
            print(f"  {i}. {archivo}")
        print(f"  0. Salir del programa")
        
        print("\n")
        seleccion = input("Selecciona una configuración (número o nombre): ").strip()
        
        # Opción de salir
        if seleccion == "0":
            print("\n👋 Saliendo del simulador...")
            break
        
        # Permitir selección por número o nombre
        if seleccion.isdigit():
            idx = int(seleccion) - 1
            if 0 <= idx < len(archivos):
                nombre_archivo = archivos[idx]
            else:
                print("❌ Número inválido.")
                continue
        else:
            nombre_archivo = seleccion if seleccion.endswith(".json") else f"{seleccion}.json"
        
        # Ejecutar el archivo
        continuar = ejecutar_archivo(nombre_archivo)
        
        if not continuar:
            break

# Ejecución principal
if __name__ == "__main__":
    main()