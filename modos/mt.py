from utils.helpers import obtener_alfabeto_default

"""
Simula una Máquina de Turing (MT)

La MT puede leer, escribir y moverse en una cinta infinita.
"""
class ModoMT:
    
    def __init__(self, data):
        self.estados = data["estados"]
        self.estado_inicial = data["estado_inicial"]
        self.estados_finales = data["estados_finales"]
        self.transiciones = data["transiciones"]

        # Inicializando la cinta con entrada y espacios en blanco
        self.cinta = list(data["entrada"]) + ["_"] * 10
        self.pos = 0
        self.estado = self.estado_inicial
        self.alfabeto = data.get("alfabeto", obtener_alfabeto_default())
        self.max_pasos = 1000  # Límite para evitar bluce infinito
    
    def ejecutar(self):
        print(f"Estado inicial: {self.estado}")
        print(f"Cinta inicial: {''.join(self.cinta[:20])}")
        print(f"Cabezal en posición: {self.pos}\n")
        
        pasos = 0
        
        while pasos < self.max_pasos:
            # Símbolo actual
            simbolo = self.cinta[self.pos]
            
            # Transición exacta
            clave = f"({self.estado}, '{simbolo}')"
            clave_comodin = f"({self.estado}, '*')"
            
            # Si no hay transición se detendra
            if clave not in self.transiciones and clave_comodin not in self.transiciones:
                break
            
            # Aplicar transición
            if clave in self.transiciones:
                nuevo_estado, escribir, mover = self.transiciones[clave]
            else:
                # Se usa el comodín *
                nuevo_estado, escribir, mover = self.transiciones[clave_comodin]
            
            # Se escribe en la cinta
            self.cinta[self.pos] = escribir
            self.estado = nuevo_estado
            
            # Mover la flecha
            if mover == "R":
                self.pos += 1
                # Aumentamos la cinta si es necesario
                if self.pos >= len(self.cinta):
                    self.cinta.append("_")
                    
            elif mover == "L" and self.pos > 0:
                self.pos -= 1
            
            # Se muestra el estado actual
            cinta_visual = ''.join(self.cinta[:min(30, len(self.cinta))])
            print(f"  Paso {pasos+1}: [{self.estado}] {cinta_visual} (pos: {self.pos})")
            
            pasos += 1
        
        print(f"\nEstado final: {self.estado}")
        print(f"Cinta final: {''.join(self.cinta[:30])}")
        
        if self.estado in self.estados_finales:
            print("Cadena ACEPTADA por la MT\n")
        else:
            print("Cadena RECHAZADA\n")