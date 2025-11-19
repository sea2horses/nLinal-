from py.functions.models.vector import Vector
from py.functions.models.matriz import Matriz
from py.functions.utils.auxiliar import a_fraccion
from fractions import Fraction


def fraction_make(input: str) -> Fraction:
    return a_fraccion(input)


def matrix_make(input: list[list[str]]) -> Matriz:
    if len(input) == 0:
        raise Exception("No se ingresaron datos")

    agreed_column_count = len(input[0])
    mat: Matriz = Matriz(len(input), agreed_column_count)
    for i, f in enumerate(input):
        if len(f) != agreed_column_count:
            raise Exception("Matrix is not consistent in its size")
        for j, c in enumerate(f):
            frac = fraction_make(c)
            mat.set(i + 1, j + 1, frac)

    return mat
