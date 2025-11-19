from typing import Any
from fractions import Fraction


def pretty_print_matrix(matrix: list[list[Fraction]], additive: str = ""):
    string = additive
    # Determine the maximum width needed for each column
    column_widths = [max(len(str(item)) for item in col)
                     for col in zip(*matrix)]

    row_count = len(matrix)
    for i, row in enumerate(matrix):
        if i == 0 and i == row_count - 1:
            string += "[ "
        elif i == 0:
            string += "┌ "
        elif i == row_count - 1:
            string += "└ "
        else:
            string += "│ "

        for j, element in enumerate(row):
            col = column_widths[j] - len(str(element))
            middle = col // 2
            # Right-align and add spacing
            string += " " * middle
            string += f"{str(element)}"
            string += " " * (col - middle + 1)

        if i == 0 and i == row_count - 1:
            string += "]  "
        elif i == 0:
            string += "┐  "
        elif i == row_count - 1:
            string += "┘  "
        else:
            string += "│  "
        string += "\n" + additive
    return string


def a_fraccion(x):
    """
    Convierte un número (decimal o fracción en string) a Fraction exacta.
    """
    try:
        if '/' in str(x):
            return Fraction(x)
        else:
            return Fraction(str(x))
    except Exception as e:
        raise ValueError(f"Entrada inválida: {x}") from e


# Estas funciones han sido deprecadas tambien debido al nuevo sistema de fracciones

# def pretty_number(num, decimals=4):
#     # Devuelve un número formateado de manera legible:
#     # - Enteros con separador de miles.
#     # - Flotantes con separador de miles y decimales limitados.
#     # - Notación científica para números muy grandes o muy pequeños.
#     # Si es int, usa separadores de miles
#     if isinstance(num, int):
#         return f"{num:,}"

#     # Si es float, decidir si usar notación científica
#     if isinstance(num, float):
#         if abs(num) != 0 and (abs(num) < 1e-4 or abs(num) >= 1e6):
#             return f"{num:.{decimals}e}"
#         else:
#             return f"{num:,.{decimals}f}".rstrip("0").rstrip(".")

#     # Por si acaso le pasan algo raro
#     return str(num)

# # Añadir tolerancia para comparaciones de punto flotante
# TOLERANCIA = 1e-10


# def es_cero(valor: float) -> bool:
#     return abs(valor) < TOLERANCIA


# def es_uno(valor: float) -> bool:
#     return abs(valor - 1) < TOLERANCIA

# Matrices de cambio, de numeros a numeros en potencia (supercript) y numeros de subscript (Para en lugar de imprimir X2, poder imprimir X₂)
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

# Esta funcion convierte todos los numeros del string a subscript


def to_subscript(string: str):
    return string.translate(SUB)  # X3 = X₃

# Esta funcion convierte todos los numeros del string a superscript


def to_superscript(string: str):
    return string.translate(SUP)  # Yo soy el numero ¹

# Mejorar la función de impresión de términos
# Para escribir un termino sin variable el argumento variable debe ser 0


# ESTA FUNCION HA SIDO DEPRECADA POR LA NUEVA CLASE DE ECUACIONES EN ECUACION.PY

# def termino_a_string(coeficiente: float, variable: int | None, es_primer_termino: bool = False):
#     nombre_variable = ""
#     if variable != None:
#         if variable <= 0:
#             raise Exception(
#                 "No se puede imprimir un termino con un numero de variable negativa")
#         nombre_variable = to_subscript(f"X{variable}")

#     if es_cero(coeficiente):
#         return ""

#     signo = ""
#     if not es_primer_termino or coeficiente < 0:
#         signo = "+ " if coeficiente >= 0 else "- "

#     coeficiente_abs = abs(coeficiente)
#     if es_uno(coeficiente_abs) and variable is not None:
#         return f"{signo}{nombre_variable}"
#     else:
#         return f"{signo}{pretty_number(coeficiente_abs)}{nombre_variable} "
