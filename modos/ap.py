from utils.helpers import obtener_alfabeto_default


"""
Simula un Autómata de Pila (AP)

El AP utiliza una pila para reconocer lenguajes libres de contexto.
"""
class ModoAP:

    def __init__(self, data):
        self.estados = data["estados"]
        self.estado_inicial = data["estado_inicial"]
        self.estados_finales = data["estados_finales"]
        self.transiciones = data["transiciones"]
        self.pila_inicial = data["pila_inicial"]
        self.entrada = data["entrada"]
        self.alfabeto = data.get("alfabeto", obtener_alfabeto_default())
        self.epsilon_simbolos = ["epsilon", "eps", "e", "", "ε"]

    def es_epsilon(self, x):
        return x in self.epsilon_simbolos

    """Las transiciones posibles."""
    def buscar_transicion(self, estado, simbolo, cima):
        claves = [
            f"({estado}, '{simbolo}', '{cima}')",
            f"({estado}, '{simbolo}', '*')",
            f"({estado}, 'epsilon', '{cima}')",
            f"({estado}, 'epsilon', '*')",
            f"({estado}, 'ε', '{cima}')",
            f"({estado}, 'ε', '*')"
        ]

        for k in claves:
            if k in self.transiciones:
                return self.transiciones[k]

        return None


    def ejecutar(self):
        estado = self.estado_inicial
        pila = [self.pila_inicial]

        print(f"\nEstado inicial: {estado}")
        print(f"Pila inicial: {pila}")
        print(f"Entrada: '{self.entrada}'\n")

        idx = 0  # índice sobre entrada

        while True:

            # símbolo actual o epsilon si ya no hay entrada
            simbolo = self.entrada[idx] if idx < len(self.entrada) else "epsilon"
            cima = pila[-1] if pila else "ε"

            trans = self.buscar_transicion(estado, simbolo, cima)

            if not trans:
                # intentar transición epsilon antes de fallar
                trans = self.buscar_transicion(estado, "epsilon", cima)

            if not trans:
                if idx < len(self.entrada):
                    print(f"No hay transición para estado={estado}, simbolo='{simbolo}', cima='{cima}'")
                    print("Cadena RECHAZADA\n")
                    return
                break  
                
            nuevo_estado, accion = trans

            # POP siempre que haya cima
            if pila:
                pila.pop()

            # PUSH según la acción
            if accion != "pop" and not self.es_epsilon(accion):
                for s in reversed(accion):
                    pila.append(s)

            print(f"Δ({estado}, '{simbolo}', '{cima}') → {nuevo_estado}, push:'{accion}', pila:{pila}")

            estado = nuevo_estado

            # Avanzar si no fue epsilon
            if simbolo != "epsilon":
                idx += 1

            # Si ya no queda entrada y no hay ε-transiciones
            if idx >= len(self.entrada):
                test = self.buscar_transicion(estado, "epsilon", cima)
                if not test:
                    break

        print(f"\nEstado final: {estado}")
        print(f"Pila final: {pila}")

        if estado in self.estados_finales:
            print("Cadena ACEPTADA\n")
        else:
            print("Cadena RECHAZADA\n")