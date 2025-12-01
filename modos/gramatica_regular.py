# modos/gramatica_regular.py
"""
Simula una Gramática Regular (Tipo 3)

Las gramáticas regulares tienen producciones de la forma:
- A → aB (lineal derecha)
- A → a (terminal)
- A → ε (epsilon)

NOTA: Para epsilon usa "epsilon", "eps", "e", "ε" o "" (cadena vacía)
"""
from collections import deque

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
    
    def derivar_bfs(self, objetivo):
        """
        Búsqueda BFS (amplitud) para encontrar derivación.
        Más robusto que DFS para gramáticas regulares.
        
        Retorna: (éxito: bool, ruta: list)
        """
        # Cola: (forma_sentencial, historial_completo)
        cola = deque([(self.simbolo_inicial, [self.simbolo_inicial])])
        visitados = {self.simbolo_inicial}
        pasos = 0
        
        while cola and pasos < self.max_pasos:
            actual, historial = cola.popleft()
            pasos += 1
            
            # ¿Alcanzamos el objetivo?
            if actual == objetivo:
                return True, historial
            
            # Poda inteligente: si ya tenemos más terminales consumidos que el objetivo
            terminales_actuales = self._contar_terminales(actual)
            if terminales_actuales > len(objetivo):
                continue
            
            # Expandir: buscar el primer (o único) no-terminal
            expandido = False
            for i, simbolo in enumerate(actual):
                if simbolo in self.producciones:
                    # Expandir este no-terminal con todas sus producciones
                    for produccion in self.producciones[simbolo]:
                        # Aplicar la producción
                        if self.es_epsilon(produccion):
                            # A → ε: eliminar el no-terminal
                            nueva = actual[:i] + actual[i+1:]
                        else:
                            # A → α: reemplazar el no-terminal
                            nueva = actual[:i] + produccion + actual[i+1:]
                        
                        # Evitar ciclos
                        if nueva not in visitados:
                            visitados.add(nueva)
                            nuevo_historial = historial + [nueva]
                            cola.append((nueva, nuevo_historial))
                    
                    expandido = True
                    # En gramáticas lineales derechas, solo expandimos el primer no-terminal
                    break
            
            # Si no hay no-terminales y no coincide, es una rama muerta
            if not expandido and actual != objetivo:
                continue
        
        return False, []
    
    def _contar_terminales(self, cadena):
        """Cuenta cuántos símbolos terminales hay en la cadena"""
        count = 0
        for simbolo in cadena:
            if simbolo not in self.producciones:
                count += 1
        return count
    
    def derivar_dfs_mejorado(self, objetivo):
        """
        DFS mejorado con mejor poda y detección de ciclos.
        Alternativa más rápida para algunas gramáticas.
        """
        
        def dfs_recursivo(actual, historial, visitados, profundidad):
            # Límite de profundidad
            if profundidad > self.max_pasos:
                return False, []
            
            # ¿Éxito?
            if actual == objetivo:
                return True, historial
            
            # Estado para evitar ciclos infinitos
            estado = (actual, profundidad % 50)  # Módulo para limitar memoria
            if estado in visitados:
                return False, []
            visitados.add(estado)
            
            # Poda: si ya excedimos la longitud objetivo con solo terminales
            if self._solo_terminales(actual) and len(actual) != len(objetivo):
                return False, []
            
            # Buscar primer no-terminal
            for i, simbolo in enumerate(actual):
                if simbolo in self.producciones:
                    # Probar cada producción
                    for produccion in self.producciones[simbolo]:
                        # Aplicar producción
                        if self.es_epsilon(produccion):
                            nueva = actual[:i] + actual[i+1:]
                        else:
                            nueva = actual[:i] + produccion + actual[i+1:]
                        
                        # Poda: no crecer indefinidamente
                        if len(nueva) > len(objetivo) + 10:
                            continue
                        
                        # Recursión
                        nuevo_historial = historial + [nueva]
                        exito, ruta = dfs_recursivo(nueva, nuevo_historial, visitados.copy(), profundidad + 1)
                        if exito:
                            return True, ruta
                    
                    # Solo expandir el primer no-terminal
                    return False, []
            
            # No hay más no-terminales
            return False, []
        
        return dfs_recursivo(self.simbolo_inicial, [self.simbolo_inicial], set(), 0)
    
    def _solo_terminales(self, cadena):
        """Verifica si la cadena solo contiene terminales"""
        for simbolo in cadena:
            if simbolo in self.producciones:
                return False
        return True
    
    def _mostrar_producciones(self):
        """Muestra todas las producciones de la gramática"""
        print("\n📐 Producciones de la gramática regular:")
        print("─" * 50)
        for no_terminal, prods in self.producciones.items():
            prod_strs = []
            for prod in prods:
                prod_mostrar = prod if not self.es_epsilon(prod) else "ε"
                prod_strs.append(prod_mostrar)
            print(f"  {no_terminal} → {' | '.join(prod_strs)}")
        print("─" * 50)
    
    def ejecutar(self):
        """Ejecuta la simulación de la gramática regular"""
        print(f"\n📝 Descripción: {self.descripcion}")
        print(f"🎯 Símbolo inicial: {self.simbolo_inicial}")
        
        # Mostrar cadena objetivo (manejar epsilon)
        if self.entrada == "":
            print(f"📥 Cadena objetivo: 'ε' (cadena vacía)")
        else:
            print(f"📥 Cadena objetivo: '{self.entrada}' (longitud: {len(self.entrada)})")
        
        # Mostrar producciones
        self._mostrar_producciones()
        
        print(f"\n{'─'*50}")
        print("Buscando derivación con BFS...")
        print(f"{'─'*50}")
        
        # Intentar derivar con BFS (más robusto)
        exito, ruta = self.derivar_bfs(self.entrada)
        
        # Si BFS falla, intentar con DFS mejorado
        if not exito:
            print("\n🔄 Intentando con DFS mejorado...")
            exito, ruta = self.derivar_dfs_mejorado(self.entrada)
        
        if exito:
            self.ruta_exitosa = ruta
            print("\n✅ La cadena PERTENECE al lenguaje generado ✅")
            print(f"\n🔍 Derivación encontrada ({len(ruta)} pasos):")
            print("─" * 50)
            
            for i, paso in enumerate(ruta):
                paso_mostrar = paso if paso != "" else "ε"
                
                if i == 0:
                    print(f"  Paso {i}: {paso_mostrar} (inicio)")
                elif i == len(ruta) - 1:
                    print(f"  Paso {i}: {paso_mostrar} ✓ (objetivo alcanzado)")
                else:
                    print(f"  Paso {i}: {paso_mostrar}")
            
            print("─" * 50)
            return True
        else:
            print(f"\n❌ La cadena NO pertenece al lenguaje")
            print(f"   (Se alcanzó el límite de {self.max_pasos} pasos o no hay derivación posible)")
            return False