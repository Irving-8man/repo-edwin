# modos/gramatica_regular.py
"""
Simula una Gramática Regular (Tipo 3)

Las gramáticas regulares tienen producciones de la forma:
- A → aB (lineal derecha)
- A → a (terminal)
- A → ε (epsilon)

NOTA: Para epsilon usa "epsilon", "eps", "e", "ε" o "" (cadena vacía)
"""

class ModoGramaticaRegular:
    
    def __init__(self, data):
        self.producciones = data.get("producciones", {})
        self.simbolo_inicial = data.get("simbolo_inicial", "S")
        self.entrada = data.get("entrada", "")
        self.alfabeto = data.get("alfabeto", [])
        self.descripcion = data.get("descripcion", "Sin descripción")
        self.max_pasos = data.get("max_pasos", 200)
        self.epsilon_simbolos = ["epsilon", "eps", "e", "", "ε"]
        
        # Para rastrear la derivación exitosa
        self.ruta_exitosa = []
        
        # Validar configuración
        self._validar_configuracion()
    
    def _validar_configuracion(self):
        """Valida que la configuración sea correcta"""
        if not self.simbolo_inicial:
            raise ValueError("❌ Falta definir el símbolo inicial")
        
        if self.simbolo_inicial not in self.producciones:
            raise ValueError(f"❌ El símbolo inicial '{self.simbolo_inicial}' no tiene producciones")
        
        # Verificar que las producciones sean de tipo regular
        for no_terminal, prods in self.producciones.items():
            if not isinstance(prods, list):
                raise ValueError(f"❌ Las producciones de '{no_terminal}' deben ser una lista")
    
    def es_epsilon(self, simbolo):
        """Verifica si un símbolo representa epsilon (cadena vacía)"""
        return simbolo in self.epsilon_simbolos
    
    def _es_terminal(self, simbolo):
        """Verifica si un símbolo es terminal (no está en producciones)"""
        return simbolo not in self.producciones
    
    def derivar(self, actual, objetivo, pasos=0, historial=None, visitados=None):
        """
        Intenta derivar la cadena objetivo desde la cadena actual.
        Retorna True si tiene éxito, guardando la ruta en self.ruta_exitosa
        """
        if historial is None:
            historial = [actual]
        if visitados is None:
            visitados = set()
        
        # Caso base: se logró derivar el objetivo
        if actual == objetivo:
            self.ruta_exitosa = historial.copy()
            return True
        
        # Detectar bucles
        estado = (actual, pasos)
        if estado in visitados:
            return False
        visitados.add(estado)
        
        # Límite de pasos
        if pasos >= self.max_pasos:
            return False
        
        # Poda: si la cadena actual es más larga que el objetivo
        if len(actual) > len(objetivo):
            return False
        
        # Intentar expandir el primer no-terminal de izquierda a derecha
        for i, simbolo in enumerate(actual):
            if simbolo in self.producciones:
                # Probar cada producción
                for produccion in self.producciones[simbolo]:
                    # Manejar epsilon
                    if self.es_epsilon(produccion):
                        nueva = actual[:i] + actual[i+1:]
                    else:
                        nueva = actual[:i] + produccion + actual[i+1:]
                    
                    # Recursión con historial
                    nuevo_historial = historial + [nueva]
                    if self.derivar(nueva, objetivo, pasos + 1, nuevo_historial, visitados):
                        return True
                
                # En gramáticas regulares, solo expandimos el primer no-terminal
                # Si no funcionó ninguna producción, retornamos False
                return False
        
        # Si no hay más no-terminales y no coincide con el objetivo
        return False
    
    def _mostrar_producciones(self):
        """Muestra todas las producciones de la gramática"""
        print("\n📐 Producciones de la gramática regular:")
        print("─" * 50)
        for no_terminal, prods in self.producciones.items():
            for prod in prods:
                prod_mostrar = prod if not self.es_epsilon(prod) else "ε"
                print(f"  {no_terminal} → {prod_mostrar}")
        print("─" * 50)
    
    def ejecutar(self):
        """Ejecuta la simulación de la gramática regular"""
        print(f"\n📝 Descripción: {self.descripcion}")
        print(f"🎯 Símbolo inicial: {self.simbolo_inicial}")
        print(f"📥 Cadena objetivo: '{self.entrada}' (longitud: {len(self.entrada)})")
        
        # Mostrar producciones
        self._mostrar_producciones()
        
        # Reiniciar ruta exitosa
        self.ruta_exitosa = []
        
        print(f"\n{'─'*50}")
        print("Buscando derivación...")
        print(f"{'─'*50}")
        
        # Intentar derivar
        if self.derivar(self.simbolo_inicial, self.entrada):
            print("\n✅ La cadena PERTENECE al lenguaje generado ✅")
            print(f"\n🔍 Derivación encontrada ({len(self.ruta_exitosa)} pasos):")
            print("─" * 50)
            
            for i, paso in enumerate(self.ruta_exitosa):
                paso_mostrar = paso if paso != "" else "ε"
                
                if i == 0:
                    print(f"  Paso {i}: {paso_mostrar} (inicio)")
                elif i == len(self.ruta_exitosa) - 1:
                    print(f"  Paso {i}: {paso_mostrar} ✓ (objetivo alcanzado)")
                else:
                    print(f"  Paso {i}: {paso_mostrar}")
            
            print("─" * 50)
        else:
            print(f"\n❌ La cadena NO pertenece al lenguaje")
            print(f"   (Se alcanzó el límite de {self.max_pasos} pasos o no hay derivación posible)")