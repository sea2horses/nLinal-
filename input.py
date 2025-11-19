from vector import Vector
from matriz import Matriz
from auxiliar import a_fraccion


def safe_input(prompt, funcion, mensaje="El input no es válido"):
    while True:
        try:
            return funcion(input(prompt))
        except:
            print(mensaje)

# Input de Numero (posibilidad decimal) que lo convierte automaticamente a fraccion


def input_numero(prompt, mensaje="Debe ingresar un numero (o fracción) válid@."):
    while True:
        try:
            return a_fraccion(input(prompt))
        except:
            print(mensaje)


def input_vector(dimension: int):
    """
    Solicita al usuario los componentes de un vector de la dimensión dada.
    Muestra el progreso y confirma el vector final.
    """
    componentes = []
    print(f"\nIngrese los {dimension} componentes del vector:")

    for i in range(1, dimension + 1):
        valor = input_numero(
            f"      Componente {i}/{dimension}: "
        )
        componentes.append(valor)

    vector = Vector(componentes)
    print(f"\nVector ingresado: {vector}\n")
    return vector


def input_matriz(filas: int, columnas: int):
    """
    Solicita al usuario los componentes de una matriz de la dimensión dada.
    Muestra el progreso y confirma la matriz final.
    """

    matriz: Matriz = Matriz(filas, columnas)
    print(f"\nIngrese los componentes de la matriz:")
    for i in range(1, filas + 1):
        print(f"    - Fila {i}")
        for j in range(1, columnas + 1):
            numero = input_numero(
                f"          Ingrese el numero en la posición {i}, {j}: ")
            matriz.set(i, j, numero)

    print(f"Matriz ingresada: \n{matriz}")
    return matriz
