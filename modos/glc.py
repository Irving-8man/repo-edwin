from utils.helpers import obtener_alfabeto_default

"""
Simula una Gramática Libre de Contexto (GLC)

Intenta derivar la cadena de entrada desde el símbolo inicial.
"""
    
class ModoGLC:
    def __init__(self, data):
        
        self.producciones = data["producciones"]
        self.simbolo_inicial = data["simbolo_inicial"]
        self.entrada = data["entrada"]
        self.alfabeto = data.get("alfabeto", obtener_alfabeto_default())
        self.max_pasos = 1000  # Este es un límite para evitar recursión infinita
    
    def derivar(self, actual, objetivo, pasos=0):
        # Si se logro el objetivo
        if actual == objetivo:
            return True
        
        # Comprobar que no se supere el limite
        if pasos > self.max_pasos:
            return False
        
        # Si la cadena actual es más larga que el objetivo y solo tiene terminales
        # hay que terminarlo
        if len(actual) > len(objetivo) * 2:
            return False
        
        # Procesando con los no-terminales
        for i, simbolo in enumerate(actual):
            if simbolo in self.producciones:
                for produccion in self.producciones[simbolo]:
                    nueva = actual[:i] + produccion + actual[i+1:]
                    
                    # Recursión
                    if self.derivar(nueva, objetivo, pasos + 1):
                        return True
        
        return False
    
    def ejecutar(self):
        print(f"Símbolo inicial: {self.simbolo_inicial}")
        print(f"Intentando derivar: '{self.entrada}'\n")
        
        if self.derivar(self.simbolo_inicial, self.entrada):
            print("La cadena PERTENECE al lenguaje generado por la GLC\n")
        else:
            print("La cadena NO pertenece al lenguaje\n")