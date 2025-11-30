# modos/afd.py
"""
Simula un Autómata Finito Determinista (AFD)

El AFD procesa una cadena de entrada símbolo por símbolo,
cambiando de estado según las transiciones definidas.
"""

class ModoAFD:
    def __init__(self, data):
        self.alfabeto = data.get("alfabeto", [])
        self.estados = data.get("estados", [])
        self.estado_inicial = data.get("estado_inicial")
        self.estados_finales = data.get("estados_finales", [])
        self.transiciones = data.get("transiciones", {})
        self.entrada = data.get("entrada", "")
        self.descripcion = data.get("descripcion", "Sin descripción")
        
        # Validar configuración
        self._validar_configuracion()
    
    def _validar_configuracion(self):
        """Valida que la configuración del AFD sea correcta"""
        if not self.estado_inicial:
            raise ValueError("❌ Falta definir el estado inicial")
        
        if self.estado_inicial not in self.estados:
            raise ValueError(f"❌ El estado inicial '{self.estado_inicial}' no está en la lista de estados")
        
        for estado_final in self.estados_finales:
            if estado_final not in self.estados:
                raise ValueError(f"❌ El estado final '{estado_final}' no está en la lista de estados")
        
        # Validar transiciones
        for estado, trans in self.transiciones.items():
            if estado not in self.estados:
                raise ValueError(f"❌ Estado '{estado}' en transiciones no está definido en estados")
            for simbolo, destino in trans.items():
                if destino not in self.estados:
                    raise ValueError(f"❌ Estado destino '{destino}' no está definido")
    
    def ejecutar(self):
        """Ejecuta la simulación del AFD"""
        estado_actual = self.estado_inicial
        COMODIN = "*"
        
        print(f"\n📝 Descripción: {self.descripcion}")
        print(f"🎯 Estado inicial: {estado_actual}")
        print(f"✅ Estados finales: {', '.join(self.estados_finales)}")
        print(f"📥 Cadena de entrada: '{self.entrada}'")
        
        if not self.entrada:
            print("\n⚠️  Cadena vacía (ε)")
            if estado_actual in self.estados_finales:
                print("✅ Cadena ACEPTADA (estado inicial es final)")
            else:
                print("❌ Cadena RECHAZADA (estado inicial no es final)")
            return
        
        print(f"\n{'─'*50}")
        print("Procesando transiciones:")
        print(f"{'─'*50}")
        
        # Procesar cada símbolo
        for i, simbolo in enumerate(self.entrada, 1):
            # Verificar si el símbolo está en el alfabeto
            if simbolo not in self.alfabeto and COMODIN not in self.alfabeto:
                print(f"⚠️  Paso {i}: '{simbolo}' no está en el alfabeto definido")
                # Puedes decidir si rechazar o continuar
            
            # Buscar transición
            if estado_actual in self.transiciones:
                if simbolo in self.transiciones[estado_actual]:
                    nuevo_estado = self.transiciones[estado_actual][simbolo]
                    print(f"  Paso {i}: δ({estado_actual}, '{simbolo}') → {nuevo_estado}")
                    estado_actual = nuevo_estado
                elif COMODIN in self.transiciones[estado_actual]:
                    nuevo_estado = self.transiciones[estado_actual][COMODIN]
                    print(f"  Paso {i}: δ({estado_actual}, '{simbolo}') → {nuevo_estado} [comodín]")
                    estado_actual = nuevo_estado
                else:
                    print(f"\n❌ No hay transición para '{simbolo}' desde estado '{estado_actual}'")
                    print(f"❌ Cadena RECHAZADA")
                    return
            else:
                print(f"\n❌ No hay transiciones definidas para el estado '{estado_actual}'")
                print(f"❌ Cadena RECHAZADA")
                return
        
        # Verificar si el estado final es de aceptación
        print(f"\n{'─'*50}")
        print(f"🏁 Estado final alcanzado: {estado_actual}")
        
        if estado_actual in self.estados_finales:
            print("✅ Cadena ACEPTADA ✅")
        else:
            print("❌ Cadena RECHAZADA (no terminó en estado de aceptación)")