from utils.helpers import obtener_alfabeto_default


"""
Simula un Autómata de Pila (AP)

El AP utiliza una pila para reconocer lenguajes libres de contexto.

NOTA: Para representar epsilon (ε) usa cualquiera de estas alternativas:
- "epsilon"
- "eps"  
- "e"
- "" (cadena vacía)
"""
class ModoAP:

    def __init__(self, data):
        self.estados = data["estados"]
        self.estado_inicial = data["estado_inicial"]
        self.estados_finales = data["estados_finales"]
        self.transiciones = data["transiciones"]
        self.pila_inicial = data["pila_inicial"]
        self.entrada = data["entrada"]
        self.alfabeto = data.get("alfabeto", obtener_alfabeto_default())
        
        # Símbolos que representan epsilon
        self.epsilon_simbolos = ["epsilon", "eps", "e", "", "ε"]
    

    def ejecutar(self):
        estado = self.estado_inicial
        pila = [self.pila_inicial]
        
        print(f"Estado inicial: {estado}")
        print(f"Pila inicial: {pila}")
        print(f"Procesando: '{self.entrada}'\n")
        
        for simbolo in self.entrada:

            if simbolo not in self.alfabeto:
                print(f"'{simbolo}' no está en el alfabeto, pero se permitirá.")
                self.alfabeto.append(simbolo)
            
            # El tope de la pila
            cima = pila[-1] if pila else "epsilon"
            
            # Buscar transición: (estado, símbolo, cima_pila)
            clave = f"({estado}, '{simbolo}', '{cima}')"
            
            if clave in self.transiciones:
                nuevo_estado, accion = self.transiciones[clave]
                
                #Comienza la pila
                
                if pila:
                    # Hacer pop si hay elementos
                    pila.pop()
                
                # Apilar nuevos símbolos (si no es pop ni epsilon)
                if accion not in ["pop", "epsilon", ""]:
                    for s in reversed(accion):
                        pila.append(s)
                
                estado = nuevo_estado
                print(f"'{simbolo}' con cima '{cima}' → Estado: {estado}, Pila: {pila}")
            else:
                print(f"No hay transición para {clave}")
                print(f"Cadena RECHAZADA\n")
                return

        print(f"\nEstado final: {estado}")
        print(f"Pila final: {pila}")
        
        if estado in self.estados_finales and (not pila or pila == [self.pila_inicial]):
            print("Cadena ACEPTADA\n")
        else:
            print("Cadena RECHAZADA\n")