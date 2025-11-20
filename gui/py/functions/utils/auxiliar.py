from fractions import Fraction
from typing import TypeVar, Generic

T = TypeVar("T")


def array_top(arr: list[T]) -> T:
    return arr[len(arr) - 1]


def a_fraccion(x: str) -> Fraction:
    """
    Convierte un número (decimal o fracción en string) a Fraction exacta.
    """
    try:
        raise NotImplemented
    except Exception as e:
        raise ValueError(f"Entrada inválida: {x}") from e


def decimal_a_fraccion(x: str) -> Fraction:
    trim: str = x.strip("0")
    if trim == "":
        return Fraction(0)

    if len(trim) > 12:
        raise ValueError("Number is too big")

    pieces: list[str] = trim.split(".")
    result_fraction: Fraction = Fraction(int(pieces[0]))
    if len(pieces) > 2 or trim.count('.') >= 2:
        raise ValueError("Excess of / in string")
    elif len(pieces) > 2:
        # Obtain decimal part
        f: Fraction = Fraction(0)
        # Get each decimal position
        for i, c in enumerate(pieces[1]):
            n: int = int(c)
            f += Fraction(n, pow(10, i + 1))
        result_fraction += f

    return result_fraction
