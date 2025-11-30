# modos/mt.py
"""
Simula una Máquina de Turing (MT) con salida detallada paso a paso.
"""

class ModoMT:
    
    def __init__(self, data):
        self.estados = data.get("estados", [])
        self.estado_inicial = data.get("estado_inicial")
        self.estados_finales = data.get("estados_finales", [])
        self.transiciones_raw = data.get("transiciones", {})
        self.entrada = data.get("entrada", "")
        self.alfabeto = data.get("alfabeto", [])
        self.descripcion = data.get("descripcion", "Sin descripción")
        self.simbolo_blanco = data.get("simbolo_blanco", "_")
        self.max_pasos = data.get("max_pasos", 1000)

        # Inicializar cinta
        self.cinta = list(self.entrada) if self.entrada else [self.simbolo_blanco]
        self.cinta += [self.simbolo_blanco] * 50
        
        self.pos = 0
        self.estado = self.estado_inicial

        # Convertir transiciones "(q0, '1')" → ('q0', '1')
        self.transiciones = {}
        for k, v in self.transiciones_raw.items():
            key = k.replace("(", "").replace(")", "")
            estado, simbolo = key.split(",")
            estado = estado.strip()
            simbolo = simbolo.strip().replace("'", "")
            self.transiciones[(estado, simbolo)] = v
        
        self._validar_configuracion()

    def _validar_configuracion(self):
        if not self.estado_inicial:
            raise ValueError("❌ Falta definir el estado inicial")
        if self.estado_inicial not in self.estados:
            raise ValueError(f"❌ El estado inicial '{self.estado_inicial}' no está en estados")

    def _visualizar_cinta(self, margen=12):
        inicio = max(0, self.pos - margen)
        fin = min(len(self.cinta), self.pos + margen + 1)
        cinta = ''.join(self.cinta[inicio:fin])
        caret = ' ' * (self.pos - inicio) + '↑'
        return cinta, caret

    def _mostrar_transiciones(self):
        print("\n📐 TRANSICIONES:")
        print("────────────────────────────────────────")
        for (q, s), (q2, w, m) in self.transiciones.items():
            print(f"δ({q}, '{s}') → ({q2}, '{w}', {m})")
        print("────────────────────────────────────────\n")

    def ejecutar(self):
        print(f"\n📝 Descripción: {self.descripcion}")
        print(f"🎯 Estado inicial: {self.estado_inicial}")
        print(f"🎉 Estados finales: {self.estados_finales}")
        print(f"📥 Entrada: '{self.entrada}'\n")

        self._mostrar_transiciones()

        pasos = 0

        # Mostrar configuración inicial
        cinta, caret = self._visualizar_cinta()
        print("CONFIGURACIÓN INICIAL")
        print("────────────────────────────────────────")
        print(f"Cinta: [{cinta}]")
        print(f"       {caret}")
        print(f"Estado: {self.estado}, Pos: {self.pos}")
        print("────────────────────────────────────────\n")

        while pasos < self.max_pasos:

            simbolo = self.cinta[self.pos]

            # Usar transición exacta o comodín
            if (self.estado, simbolo) in self.transiciones:
                nuevo_estado, escribir, mover = self.transiciones[(self.estado, simbolo)]
            elif (self.estado, "*") in self.transiciones:
                nuevo_estado, escribir, mover = self.transiciones[(self.estado, "*")]
            else:
                print(f"⏹️  Paso {pasos + 1}: sin transición para ({self.estado}, '{simbolo}')")
                break

            simbolo_prev = simbolo

            # ESCRIBIR
            self.cinta[self.pos] = escribir

            # CAMBIAR ESTADO
            estado_prev = self.estado
            self.estado = nuevo_estado

            # MOVER CABEZAL
            if mover == "R":
                self.pos += 1
                if self.pos >= len(self.cinta):
                    self.cinta.append(self.simbolo_blanco)

            elif mover == "L":
                if self.pos == 0:
                    # EXTENDER CINTA A LA IZQUIERDA
                    self.cinta.insert(0, self.simbolo_blanco)
                    # El cabezal queda en 0 automáticamente
                else:
                    self.pos -= 1

            # MOVIMIENTO S → no mover

            pasos += 1

            # IMPRIMIR ESTADO DEL PASO
            cinta, caret = self._visualizar_cinta()
            print(f"Paso {pasos}: δ({estado_prev}, '{simbolo_prev}') → ({nuevo_estado}, '{escribir}', {mover})")
            print(f"        [{cinta}]")
            print(f"        {caret}\n")

            if self.estado in self.estados_finales:
                print(f"✔ Estado final '{self.estado}' alcanzado.\n")
                break

        # Mostrar cinta final
        cinta_final = ''.join(self.cinta).rstrip(self.simbolo_blanco)
        if cinta_final == "":
            cinta_final = self.simbolo_blanco

        print("\n────────────────────────────────────────")
        print("CONFIGURACIÓN FINAL")
        print(f"Cinta: [{cinta_final}]")
        print(f"Estado final: {self.estado}")
        print(f"Pasos ejecutados: {pasos}")
        print("────────────────────────────────────────")

        if self.estado in self.estados_finales:
            print("✅ Cadena ACEPTADA")
        else:
            print("❌ Cadena RECHAZADA")
