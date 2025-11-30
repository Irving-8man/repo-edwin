# modos/ap.py
"""
Simula un Autómata de Pila (AP)

El AP utiliza una pila para reconocer lenguajes libres de contexto.
Acepta por estado final (no por pila vacía).
"""

class ModoAP:
    def __init__(self, data):
        self.estados = data.get("estados", [])
        self.estado_inicial = data.get("estado_inicial")
        self.estados_finales = data.get("estados_finales", [])
        self.transiciones = data.get("transiciones", {})
        self.pila_inicial = data.get("pila_inicial", "Z")
        self.entrada = data.get("entrada", "")
        self.alfabeto = data.get("alfabeto", [])
        self.descripcion = data.get("descripcion", "Sin descripción")
        self.epsilon_simbolos = ["epsilon", "eps", "e", "", "ε"]
        self.max_pasos = data.get("max_pasos", 500)
        
        # Validar configuración
        self._validar_configuracion()
    
    def _validar_configuracion(self):
        """Valida que la configuración del AP sea correcta"""
        if not self.estado_inicial:
            raise ValueError("❌ Falta definir el estado inicial")
        
        if self.estado_inicial not in self.estados:
            raise ValueError(f"❌ El estado inicial '{self.estado_inicial}' no está en la lista de estados")
        
        for estado_final in self.estados_finales:
            if estado_final not in self.estados:
                raise ValueError(f"❌ El estado final '{estado_final}' no está en la lista de estados")
    
    def es_epsilon(self, x):
        """Verifica si un símbolo representa epsilon"""
        return x in self.epsilon_simbolos
    
    def buscar_transicion(self, estado, simbolo, cima):
        """
        Busca una transición válida en el siguiente orden de prioridad:
        1. (estado, símbolo, cima)
        2. (estado, símbolo, *)
        3. (estado, epsilon, cima)
        4. (estado, epsilon, *)
        """
        claves = [
            f"({estado}, '{simbolo}', '{cima}')",
            f"({estado}, '{simbolo}', '*')",
            f"({estado}, 'epsilon', '{cima}')",
            f"({estado}, 'epsilon', '*')",
            f"({estado}, 'ε', '{cima}')",
            f"({estado}, 'ε', '*')"
        ]
        
        for clave in claves:
            if clave in self.transiciones:
                return self.transiciones[clave]
        
        return None
    
    def _mostrar_transiciones(self):
        """Muestra todas las transiciones del autómata"""
        print("\n📐 Transiciones del Autómata de Pila:")
        print("─" * 70)
        for trans, (nuevo_estado, accion) in self.transiciones.items():
            accion_mostrar = accion if not self.es_epsilon(accion) else "ε"
            print(f"  δ{trans} → ({nuevo_estado}, {accion_mostrar})")
        print("─" * 70)
    
    def ejecutar(self):
        """Ejecuta la simulación del Autómata de Pila"""
        print(f"\n📝 Descripción: {self.descripcion}")
        print(f"🎯 Estado inicial: {self.estado_inicial}")
        print(f"✅ Estados finales: {', '.join(self.estados_finales)}")
        print(f"📚 Símbolo inicial de pila: {self.pila_inicial}")
        print(f"📥 Cadena de entrada: '{self.entrada}' (longitud: {len(self.entrada)})")
        
        # Mostrar transiciones
        self._mostrar_transiciones()
        
        # Inicializar configuración
        estado = self.estado_inicial
        pila = [self.pila_inicial]
        idx = 0  # Índice en la cadena de entrada
        pasos = 0
        
        print(f"\n{'─'*70}")
        print(f"Configuración inicial: ({estado}, '{self.entrada}', {pila})")
        print(f"{'─'*70}")
        print("Procesando transiciones:\n")
        
        # Procesar la entrada
        while pasos < self.max_pasos:
            pasos += 1
            
            # Determinar símbolo actual
            if idx < len(self.entrada):
                simbolo = self.entrada[idx]
            else:
                simbolo = "epsilon"
            
            # Obtener cima de la pila
            cima = pila[-1] if pila else "ε"
            
            # Buscar transición
            trans = self.buscar_transicion(estado, simbolo, cima)
            
            # Si no hay transición con el símbolo actual, intentar epsilon
            if not trans and simbolo != "epsilon":
                trans_epsilon = self.buscar_transicion(estado, "epsilon", cima)
                if trans_epsilon:
                    trans = trans_epsilon
                    simbolo = "epsilon"  # Marcar que usamos transición epsilon
            
            # Si aún no hay transición, terminar
            if not trans:
                if idx < len(self.entrada):
                    print(f"  Paso {pasos}: ❌ No hay transición desde ({estado}, '{simbolo}', '{cima}')")
                    print(f"\n{'─'*70}")
                    print(f"❌ Cadena RECHAZADA (sin transición válida)")
                    return
                else:
                    # Ya no hay entrada, verificar si estamos en estado final
                    break
            
            # Aplicar transición
            nuevo_estado, accion = trans
            
            # Hacer POP de la cima
            if pila:
                pila.pop()
            
            # Hacer PUSH según la acción
            if accion != "pop" and not self.es_epsilon(accion):
                # Apilar de derecha a izquierda para mantener orden correcto
                for simbolo_pila in reversed(accion):
                    pila.append(simbolo_pila)
            
            # Mostrar paso
            entrada_restante = self.entrada[idx:] if idx < len(self.entrada) else "ε"
            simbolo_mostrar = simbolo if simbolo != "epsilon" else "ε"
            accion_mostrar = accion if not self.es_epsilon(accion) else "ε"
            
            print(f"  Paso {pasos}: δ({estado}, '{simbolo_mostrar}', '{cima}') → ({nuevo_estado}, {accion_mostrar})")
            print(f"           Configuración: ({nuevo_estado}, '{entrada_restante}', {pila})")
            
            # Actualizar estado
            estado = nuevo_estado
            
            # Avanzar en la entrada solo si NO fue una transición epsilon
            if simbolo != "epsilon":
                idx += 1
            
            # Si terminamos de leer la entrada
            if idx >= len(self.entrada):
                # Intentar transiciones epsilon mientras sea posible
                trans_epsilon = self.buscar_transicion(estado, "epsilon", pila[-1] if pila else "ε")
                if not trans_epsilon:
                    break
        
        # Verificar aceptación
        print(f"\n{'─'*70}")
        print(f"🏁 Configuración final: ({estado}, entrada consumida, {pila})")
        print(f"{'─'*70}")
        
        if estado in self.estados_finales:
            print("✅ Cadena ACEPTADA ✅")
        else:
            print(f"❌ Cadena RECHAZADA (estado '{estado}' no es final)")
        
        if pasos >= self.max_pasos:
            print(f"⚠️  Advertencia: Se alcanzó el límite de {self.max_pasos} pasos")