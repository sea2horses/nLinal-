from input import safe_input
from collections.abc import Callable


class Menu:
    options: list[tuple[str, Callable]] = []

    def __init__(self, opts: list[tuple[str, Callable]] | None = None) -> None:
        self.options = opts if opts is not None else []

    def showget(self):
        if len(self.options) == 0:
            print("No options to show")
            return
        else:
            for i, o in enumerate(self.options):
                print(f"{i + 1} | {o[0]}")

        select = safe_input("\n> ", funcion=int)
        if select <= 0 or select > len(self.options):
            print("Opcion Inválida!")
        else:
            self.options[select - 1][1]()
