from fractions import Fraction
from auxiliar import a_fraccion


class Termino:
    coeficiente: str
    variable: str
    negativo: bool

    def __init__(self, coeficiente, variable="", negativo=False):

        str_coeficiente: str

        self.negativo = negativo
        if isinstance(coeficiente, (Fraction, int, float)):
            fraccion_coeficiente: Fraction = a_fraccion(coeficiente)
            if fraccion_coeficiente < 0:
                # Si nos dan negativo = True, pero el coeficiente es -2
                # volteamos para que se vuelva + 2
                self.negativo = True
                str_coeficiente = str(fraccion_coeficiente * -1)
            else:
                str_coeficiente = str(fraccion_coeficiente)
        else:
            str_coeficiente = coeficiente

        self.coeficiente = str_coeficiente
        self.variable = variable

    def __str__(self):
        if self.coeficiente == "0" and self.variable != "":
            return ""

        coef = "" if self.coeficiente == "1" and self.variable != "" else str(
            self.coeficiente)
        if self.negativo:
            return f"- {coef}{self.variable}".strip()
        return f"+ {coef}{self.variable}".strip()


class Ecuacion:
    lado_izquierdo: list[Termino]
    lado_derecho: list[Termino]

    def __init__(self):
        self.lado_izquierdo = []
        self.lado_derecho = []

    def agregar_termino(self, termino: Termino, lado="izquierdo"):
        if lado == "izquierdo":
            self.lado_izquierdo.append(termino)
        else:
            self.lado_derecho.append(termino)

    def __str__(self):
        def lado_str(lado):
            if not lado:
                return "0"
            s = " ".join(str(t) for t in lado)
            s = s.lstrip("+ ").replace("+ -", "- ")
            return s

        return f"{lado_str(self.lado_izquierdo)} = {lado_str(self.lado_derecho)}"
