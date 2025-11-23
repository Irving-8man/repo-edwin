import string
import sys

"""
Retorna una lista de caracteres permitidos
"""
def obtener_alfabeto_default():
    return [chr(i) for i in range(sys.maxunicode + 1)]