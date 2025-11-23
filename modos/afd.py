from utils.helpers import obtener_alfabeto_default

"""
Simula un Autómata Finito Determinista (AFD)

El AFD procesa una cadena de entrada símbolo por símbolo,
cambiando de estado según las transiciones definidas.
"""

class ModoAFD:

    def __init__(self, data):
        self.alfabeto = data.get("alfabeto", obtener_alfabeto_default())
        self.estados = data["estados"]
        self.estado_inicial = data["estado_inicial"]
        self.estados_finales = data["estados_finales"]
        self.transiciones = data["transiciones"]
        self.entrada = data["entrada"]
    


    def ejecutar(self):
        estado = self.estado_inicial
        COMODIN = "*"
        print(f"Estado inicial: {estado}")
        print(f"Procesando: '{self.entrada}'\n")

        
        for simbolo in self.entrada:

            # Si el simbolo no esta en el alfabeto
            if simbolo not in self.alfabeto:
                print(f"'{simbolo}' no esta en el alfabeto. Se agregará automáticamente.")
                self.alfabeto.append(simbolo)
            
            # Buscar transición de nodos
            if simbolo in self.transiciones.get(estado, {}):
                estado = self.transiciones[estado][simbolo]

            elif COMODIN in self.transiciones.get(estado, {}):
                estado = self.transiciones[estado]["*"]

            else:
                print(f"No hay transición para '{simbolo}' desde estado '{estado}'.")
                print(f"Cadena RECHAZADA\n")
                return
            
            print(f"  '{simbolo}' → Estado: {estado}")
        
        print(f"\nEstado final: {estado}")
        if estado in self.estados_finales:
            print("Cadena ACEPTADA\n")
        else:
            print("Cadena RECHAZADA (no es estado final)\n")