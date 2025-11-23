from utils.helpers import obtener_alfabeto_default

"""
Simula una Gramática Regular

Similar a GLC pero con restricciones en las producciones.

NOTA: Para epsilon usa "epsilon", "eps", "e", o "" (cadena vacía)
"""
class ModoGramaticaRegular:
    
    def __init__(self, data):
        self.producciones = data["producciones"]
        self.simbolo_inicial = data["simbolo_inicial"]
        self.entrada = data["entrada"]
        self.alfabeto = data.get("alfabeto", obtener_alfabeto_default())
        self.max_pasos = 1000 # Pasos maximos
        self.epsilon_simbolos = ["epsilon", "eps", "e", "", "ε"]
    
    """
    Verifica si un símbolo representa epsilon (cadena vacía)
    """
    def es_epsilon(self, simbolo):
        return simbolo in self.epsilon_simbolos
    

    def derivar(self, actual, objetivo, pasos=0):
        if actual == objetivo:
            return True
        
        if len(actual) > len(objetivo) or pasos > self.max_pasos:
            return False
        
        for i, simbolo in enumerate(actual):
            if simbolo in self.producciones:
                for produccion in self.producciones[simbolo]:

                    # Si es epsilon, eliminar el no-terminal
                    if self.es_epsilon(produccion):
                        nueva = actual[:i] + actual[i+1:]
                    else:
                        # Aplicacion normal
                        nueva = actual[:i] + produccion + actual[i+1:]
                    
                    if self.derivar(nueva, objetivo, pasos + 1):
                        return True
        
        return False
    
    def ejecutar(self):
        print(f"Símbolo inicial: {self.simbolo_inicial}")
        print(f"Probando cadena: '{self.entrada}'\n")
        
        if self.derivar(self.simbolo_inicial, self.entrada):
            print("La cadena PERTENECE al lenguaje\n")
        else:
            print("La cadena NO pertenece al lenguaje\n")
