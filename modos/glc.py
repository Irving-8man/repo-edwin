# modos/glc.py
"""
Simula una Gramática Libre de Contexto (GLC)

Intenta derivar la cadena de entrada desde el símbolo inicial,
mostrando todos los pasos de derivación.
"""

class ModoGLC:
    def __init__(self, data):
        self.producciones = data.get("producciones", {})
        self.simbolo_inicial = data.get("simbolo_inicial", "S")
        self.entrada = data.get("entrada", "")
        self.alfabeto = data.get("alfabeto", [])
        self.descripcion = data.get("descripcion", "Sin descripción")
        self.max_pasos = data.get("max_pasos", 100)
        
        # Para rastrear la derivación exitosa
        self.ruta_exitosa = []
        
        # Validar configuración
        self._validar_configuracion()
    
    def _validar_configuracion(self):
        """Valida que la configuración de la GLC sea correcta"""
        if not self.simbolo_inicial:
            raise ValueError("❌ Falta definir el símbolo inicial")
        
        if self.simbolo_inicial not in self.producciones:
            raise ValueError(f"❌ El símbolo inicial '{self.simbolo_inicial}' no tiene producciones definidas")
        
        # Verificar que las producciones sean válidas
        for no_terminal, prods in self.producciones.items():
            if not isinstance(prods, list):
                raise ValueError(f"❌ Las producciones de '{no_terminal}' deben ser una lista")
    
    def _es_terminal(self, simbolo):
        """Verifica si un símbolo es terminal (no está en producciones)"""
        return simbolo not in self.producciones
    
    def _tiene_no_terminales(self, cadena):
        """Verifica si una cadena contiene símbolos no terminales"""
        for simbolo in cadena:
            if not self._es_terminal(simbolo):
                return True
        return False
    
    def derivar(self, actual, objetivo, pasos=0, historial=None, visitados=None):
        """
        Intenta derivar la cadena objetivo desde la cadena actual.
        Retorna True si tiene éxito, guardando la ruta en self.ruta_exitosa
        """
        if historial is None:
            historial = [actual]
        if visitados is None:
            visitados = set()
        
        # Manejar epsilon (cadena vacía)
        actual_procesada = actual.replace("ε", "").replace("epsilon", "")
        
        # Caso base: se logró derivar el objetivo
        if actual_procesada == objetivo:
            self.ruta_exitosa = historial.copy()
            return True
        
        # Detectar bucles: si ya visitamos esta configuración
        estado = (actual_procesada, pasos)
        if estado in visitados:
            return False
        visitados.add(estado)
        
        # Límite de pasos para evitar bucles infinitos
        if pasos >= self.max_pasos:
            return False
        
        # Poda: si la cadena actual es más larga que el objetivo y solo tiene terminales
        if not self._tiene_no_terminales(actual_procesada) and actual_procesada != objetivo:
            return False
        
        # Poda adicional: si ya es muy larga
        if len(actual_procesada) > len(objetivo) * 2:
            return False
        
        # Contar no-terminales para priorizar expansiones
        num_no_terminales = sum(1 for c in actual if not self._es_terminal(c))
        
        # Poda: si hay demasiados no-terminales, probablemente no lleguemos
        if num_no_terminales > len(objetivo):
            return False
        
        # Intentar reemplazar cada no-terminal en la cadena
        # Estrategia: expandir de izquierda a derecha
        for i, simbolo in enumerate(actual):
            if simbolo in self.producciones:
                # Probar cada producción posible
                for produccion in self.producciones[simbolo]:
                    # Construir nueva cadena
                    nueva = actual[:i] + produccion + actual[i+1:]
                    
                    # Recursión con historial actualizado
                    nuevo_historial = historial + [nueva]
                    if self.derivar(nueva, objetivo, pasos + 1, nuevo_historial, visitados):
                        return True
        
        return False
    
    def _mostrar_producciones(self):
        """Muestra todas las producciones de la gramática"""
        print("\n📐 Producciones de la gramática:")
        print("─" * 50)
        for no_terminal, prods in self.producciones.items():
            for prod in prods:
                prod_mostrar = prod if prod not in ["epsilon", "ε", ""] else "ε"
                print(f"  {no_terminal} → {prod_mostrar}")
        print("─" * 50)
    
    def ejecutar(self):
        """Ejecuta la simulación de la GLC"""
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
            print("\n✅ La cadena PERTENECE al lenguaje generado por la GLC ✅")
            print(f"\n🔍 Derivación encontrada ({len(self.ruta_exitosa)} pasos):")
            print("─" * 50)
            
            for i, paso in enumerate(self.ruta_exitosa):
                paso_mostrar = paso.replace("epsilon", "ε").replace("ε", "ε" if paso in ["epsilon", "ε"] else paso)
                if paso_mostrar == "":
                    paso_mostrar = "ε"
                
                if i == 0:
                    print(f"  Paso {i}: {paso_mostrar} (inicio)")
                elif i == len(self.ruta_exitosa) - 1:
                    print(f"  Paso {i}: {paso_mostrar} ✓ (objetivo alcanzado)")
                else:
                    print(f"  Paso {i}: {paso_mostrar}")
            
            print("─" * 50)
        else:
            print(f"\n❌ La cadena NO pertenece al lenguaje")
            print(f"   (Se alcanzó el límite de {self.max_pasos} pasos sin encontrar derivación)")