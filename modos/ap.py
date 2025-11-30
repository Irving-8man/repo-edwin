# modos/ap.py
"""
Simula un Autómata de Pila (AP)

El AP utiliza una pila para reconocer lenguajes libres de contexto.
Acepta por estado final Y entrada completamente consumida.
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
        Busca una transición válida.
        Retorna: (nuevo_estado, accion, clave) o None
        """
        # Buscar transición exacta primero
        clave_exacta = f"({estado}, '{simbolo}', '{cima}')"
        if clave_exacta in self.transiciones:
            nuevo_estado, accion = self.transiciones[clave_exacta]
            return (nuevo_estado, accion, clave_exacta)
        
        # Buscar con comodín en cima
        clave_comodin = f"({estado}, '{simbolo}', '*')"
        if clave_comodin in self.transiciones:
            nuevo_estado, accion = self.transiciones[clave_comodin]
            return (nuevo_estado, accion, clave_comodin)
        
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
            
            # Obtener cima de la pila
            cima = pila[-1] if pila else "ε"
            
            # REGLA CLAVE: Solo usar epsilon si NO hay más entrada
            if idx < len(self.entrada):
                # Hay entrada por procesar
                simbolo = self.entrada[idx]
                resultado = self.buscar_transicion(estado, simbolo, cima)
                
                if resultado is None:
                    print(f"  Paso {pasos}: ❌ No hay transición desde ({estado}, '{simbolo}', '{cima}')")
                    print(f"\n{'─'*70}")
                    print(f"❌ Cadena RECHAZADA (sin transición válida)")
                    print(f"   Quedaron {len(self.entrada) - idx} símbolos sin procesar: '{self.entrada[idx:]}'")
                    return
                
                nuevo_estado, accion, clave = resultado
                simbolo_usado = simbolo
                avanzar = True
                
            else:
                # NO hay más entrada, buscar transición epsilon
                for eps in ['epsilon', 'ε']:
                    resultado = self.buscar_transicion(estado, eps, cima)
                    if resultado:
                        break
                
                if resultado is None:
                    # No hay transición epsilon, terminamos
                    break
                
                nuevo_estado, accion, clave = resultado
                simbolo_usado = "ε"
                avanzar = False
            
            # APLICAR TRANSICIÓN A LA PILA
            # Siempre hacer POP de la cima primero
            if pila:
                pila.pop()
            
            # Luego PUSH según la acción
            if accion == "pop":
                # Solo pop, no push nada
                pass
            elif not self.es_epsilon(accion):
                # Push los símbolos en orden inverso (para que queden en orden correcto)
                for simbolo_pila in reversed(accion):
                    pila.append(simbolo_pila)
            # Si accion es epsilon, solo hicimos pop
            
            # Calcular entrada restante
            if avanzar:
                resto = self.entrada[idx + 1:]
            else:
                resto = self.entrada[idx:] if idx < len(self.entrada) else ""
            
            # Mostrar paso
            acc_show = accion if not self.es_epsilon(accion) else "ε"
            
            print(f"  Paso {pasos}: δ{clave} → ({nuevo_estado}, {acc_show})")
            print(f"           Configuración: ({nuevo_estado}, '{resto}', {pila})")
            
            # Actualizar estado
            estado = nuevo_estado
            
            # Avanzar en la entrada SOLO si consumimos un símbolo real
            if avanzar:
                idx += 1
        
        # Verificar aceptación
        print(f"\n{'─'*70}")
        print(f"🏁 Configuración final: ({estado}, '{self.entrada[idx:]}', {pila})")
        print(f"🔍 Símbolos procesados: {idx}/{len(self.entrada)}")
        print(f"{'─'*70}")
        
        # CRITERIO DE ACEPTACIÓN: 
        # 1. Estado final
        # 2. TODA la entrada consumida
        if estado in self.estados_finales and idx == len(self.entrada):
            print("✅ Cadena ACEPTADA ✅")
        elif estado not in self.estados_finales:
            print(f"❌ Cadena RECHAZADA (estado '{estado}' no es final)")
        elif idx < len(self.entrada):
            simbolos_restantes = len(self.entrada) - idx
            print(f"❌ Cadena RECHAZADA (quedan {simbolos_restantes} símbolos sin procesar: '{self.entrada[idx:]}')")
        else:
            print("❌ Cadena RECHAZADA")
        
        if pasos >= self.max_pasos:
            print(f"⚠️  Advertencia: Se alcanzó el límite de {self.max_pasos} pasos")