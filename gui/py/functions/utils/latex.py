from py.functions.models.matriz import Matriz
from py.functions.models.vector import Vector
from fractions import Fraction
import re


class LatexBuffer():
    stdout = ""

    def __init__(self):
        pass

    def clear(self):
        self.stdout = ""

    def write(self, msg):
        self.stdout += text(msg)

    def writeln(self, msg):
        self.stdout += text(msg) + newline()

    def writelatex(self, latex):
        self.stdout += latex


LATEX_STDOUT = LatexBuffer()


def fraction(frac: Fraction, force_sign: bool = False) -> str:
    latex = ""

    if force_sign and frac >= 0:
        latex += "+"

    if frac.denominator == 1:
        latex += str(frac.numerator)
    else:
        if frac < 0:
            latex += "-"
        latex += f"\\frac{{ {abs(frac.numerator)} }}{{ {frac.denominator} }}"

    return latex


def matrix(mat: Matriz) -> str:

    latex = "\\left[\\begin{array}"

    # Calcular linea
    if mat.linea != -1 and mat.linea < mat.columnas:
        lc = "c" * mat.linea
        rc = "c" * (mat.columnas - mat.linea)
        latex += "{" + lc + "|" + rc + "}"
    else:
        latex += "{" + "c" * mat.columnas + "}"

    # Meter todos los elementos
    for i in range(1, mat.filas + 1):
        for j in range(1, mat.columnas + 1):
            if j != 1:
                latex += " & "
            latex += fraction(mat.at(i, j))
        latex += "\\\\"

    # Terminar
    latex += "\\end{array}\\right]"
    return latex


def vector(vec: Vector) -> str:
    latex = "\\begin{bmatrix}"

    for c in vec.componentes:
        latex += fraction(c) + "\\"

    latex += "\\end{bmatrix}"
    return latex


# Mapping per latex table
_LATEX_MAP = {
    '#': r'\#',
    '$': r'\$',
    '%': r'\%',
    '&': r'\&',
    '~': r'\~{}',       # \~ is an accent; {} makes it a standalone tilde
    '_': r'\_',
    '^': r'\^{}',       # same idea for caret
    '{': r'\{',
    '}': r'\}',
    '>': r'$>$',
    '<': r'$<$',
    '\\': r'$\backslash$',
}

# Match any of the target characters (note the escaped backslash at the end)
_PATTERN = re.compile(r'[#$%&~_^{}><\\]')


def sanitize_text(raw_text: str) -> str:
    return _PATTERN.sub(lambda m: _LATEX_MAP[m.group(0)], raw_text)


def text(msg: str) -> str:
    lines = msg.splitlines()

    latex = ""
    for i, line in enumerate(lines):
        if i != 0:
            latex += newline()
        latex += "\\text{" + sanitize_text(line) + "}"

    return latex


def newline() -> str:
    return "\\\\ "

# Notation stuff


def superscript(msg: str) -> str:
    return "^{" + msg + "}"


def subscript(msg: str) -> str:
    return "_{" + msg + "}"


def cdot() -> str:
    return "\\cdot "


def frac(num: str, den: str) -> str:
    return "\\frac{" + num + "}{" + den + "}"


def larrow() -> str:
    return "\\gets "


def rarrow() -> str:
    return "\\to "


def barrow() -> str:
    return "\\leftrightarrow "


def term(varname: str, coefficent: Fraction = Fraction(1), forcesign: bool = False, hideOne: bool = True, ignoreZero: bool = False):
    if coefficent == 0 and ignoreZero:
        return ""

    latex = ""
    if forcesign and coefficent >= 0:
        latex += "+"

    if coefficent != 1 or not hideOne:
        latex += fraction(coefficent)

    latex += varname
    return latex


def indexedvar(varname: str, index: int):
    return varname + "_{" + str(index) + "} "
