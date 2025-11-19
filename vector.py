from fractions import Fraction
from auxiliar import a_fraccion


class Vector:
    componentes: list[Fraction]
    dimension: int

    def __init__(self, componentes):
        if not componentes:
            raise Exception("Un vector no puede estar vacío.")

        self.componentes: list[Fraction] = list(
            a_fraccion(comp) for comp in componentes)
        self.dimension = len(componentes)

    def at(self, indice: int) -> Fraction:
        """
        Devuelve el valor en la posición `indice` (1-indexado).
        """
        if indice <= 0 or indice > self.dimension:
            raise Exception(
                f"Índice fuera de rango: se pidió el componente {indice} de un vector de dimensión {self.dimension}")
        return self.componentes[indice - 1]

    def set(self, indice: int, valor: float):
        """
        Establece el valor en la posición `indice` (1-indexado).
        """
        if indice <= 0 or indice > self.dimension:
            raise Exception(
                f"Índice fuera de rango: se intentó modificar el componente {indice} en un vector de dimensión {self.dimension}")
        self.componentes[indice - 1] = a_fraccion(valor)

    def __str__(self) -> str:
        """
        Devuelve una representación legible del vector.
        Ejemplo: [1, 2.5, -3.75]
        """
        return "(" + ", ".join(str(x) for x in self.componentes) + ")"

    def __len__(self) -> int:
        """
        Permite usar len(vector) para obtener su dimensión.
        """
        return self.dimension

    def copy(self):
        """
        Devuelve una copia del vector.
        """
        return Vector(self.componentes.copy())
