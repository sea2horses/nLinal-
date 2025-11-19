import py.functions.utils.latex as latex
import py.functions.utils.input as input

import py.functions.operations.funciones as fn
import py.functions.operations.operaciones as op


def resolver_sistema_por_gauss_jordan(mat: list[list[str]], ecuaciones: int, incognitas: int) -> str:
    accmat = input.matrix_make(mat)
    latex.LATEX_STDOUT.clear()
    fn.resolver_sistema(accmat, ecuaciones, incognitas)
    return latex.LATEX_STDOUT.stdout
