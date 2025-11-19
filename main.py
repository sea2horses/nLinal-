# Importación de clases y funciones necesarias para la aplicación principal
from matriz import Matriz  # Clase para manejar matrices
from funciones import *    # Funciones principales de álgebra lineal
from operaciones import *
# Utilidades para formato y comparación
from auxiliar import to_subscript
# Funciones para entrada de datos
from input import safe_input, input_vector, input_matriz, input_numero
from fractions import Fraction
from menu import Menu
from sys import exit

# -------------------------------
# Menú para resolver sistemas de ecuaciones lineales
# -------------------------------


def menu_sistema_ecuaciones():
    """
    Menú interactivo para ingresar y resolver un sistema de ecuaciones lineales.
    Permite al usuario ingresar la cantidad de incógnitas y ecuaciones, así como los coeficientes y resultados.
    Utiliza la función resolver_sistema para mostrar la solución paso a paso.
    """
    print("--- CALCULADORA DE SISTEMA DE ECUACIONES (AX=B) ---")  # Título del menú

    # Solicitar cantidad de incógnitas al usuario
    incognitas: int = safe_input(
        "Ingrese la cantidad de incognitas: ", funcion=int)
    # Solicitar cantidad de ecuaciones al usuario
    ecuaciones: int = safe_input(
        "Ingrese la cantidad de ecuaciones: ", funcion=int)

    # La matriz aumentada tiene incognitas + 1 columnas (última columna = resultados)
    matriz: Matriz = Matriz(ecuaciones, incognitas + 1)
    num_columnas = incognitas + 1  # Número total de columnas

    # Solicitar coeficientes y resultados para cada ecuación
    for fila in range(1, ecuaciones + 1):
        print(f"\n-- Fila #{fila} --\n")  # Indicar la fila actual
        for columna in range(1, num_columnas + 1):
            # Si es la última columna, pedir el resultado
            prompt: str = to_subscript(
                f"Ingrese el coeficiente de X{columna}: ") if columna != incognitas + 1 else "Ingrese el resultado: "
            # Leer el valor y guardarlo en la matriz
            valor: Fraction = input_numero(prompt)
            matriz.set(fila, columna, valor)

    # Mostrar la matriz inicial ingresada
    print(f"Matriz Inicial:\n{matriz}")

    # Resolver el sistema usando el método de reducción escalonada
    print("\n=== RESOLUCION ===")
    resolver_sistema(matriz, ecuaciones, incognitas)


def menu_sistema_ecuaciones_cramer():
    """
    Menú interactivo para ingresar y resolver un sistema de ecuaciones lineales.
    Permite al usuario ingresar la cantidad de incógnitas y ecuaciones, así como los coeficientes y resultados.
    Utiliza la función resolver_sistema para mostrar la solución paso a paso.
    """
    print("--- CALCULADORA DE SISTEMA DE ECUACIONES (AX=B) ---")  # Título del menú

    # Solicitar cantidad de incógnitas al usuario
    incognitas: int = safe_input(
        "Ingrese la cantidad de incognitas: ", funcion=int)
    # Solicitar cantidad de ecuaciones al usuario
    ecuaciones: int = safe_input(
        "Ingrese la cantidad de ecuaciones: ", funcion=int)

    # La matriz aumentada tiene incognitas + 1 columnas (última columna = resultados)
    matriz: Matriz = Matriz(ecuaciones, incognitas + 1)
    num_columnas = incognitas + 1  # Número total de columnas

    # Solicitar coeficientes y resultados para cada ecuación
    for fila in range(1, ecuaciones + 1):
        print(f"\n-- Fila #{fila} --\n")  # Indicar la fila actual
        for columna in range(1, num_columnas + 1):
            # Si es la última columna, pedir el resultado
            prompt: str = to_subscript(
                f"Ingrese el coeficiente de X{columna}: ") if columna != incognitas + 1 else "Ingrese el resultado: "
            # Leer el valor y guardarlo en la matriz
            valor: Fraction = input_numero(prompt)
            matriz.set(fila, columna, valor)

    # Mostrar la matriz inicial ingresada
    print(f"Matriz Inicial:\n{matriz}")
    # Resolver el sistema usando el método de cramer
    print("\n=== RESOLUCION ===")
    resolver_sistema_cramer(matriz, ecuaciones, incognitas)


# -------------------------------
# Menú para combinación lineal de vectores
# -------------------------------


def menu_combinacion_lineal():
    """
    Menú interactivo para calcular la combinación lineal de un conjunto de vectores.
    Permite al usuario ingresar la dimensión, los vectores y el vector resultado.
    Utiliza la función combinacion_lineal para mostrar el proceso y la solución.
    """
    print("--- CALCULADORA DE COMBINACION LINEAL DE VECTORES ---")  # Título del menú

    # Solicitar dimensión de los vectores
    dimension: int = safe_input("Dimension de los vectores: ", funcion=int)

    # Solicitar cantidad de vectores
    cantidad_vectores: int = safe_input(
        "Numero de vectores a combinar (no incluye el vector resultado): ", funcion=int)
    vectores_incognita: list[Vector] = []  # Lista para almacenar los vectores

    # Ingresar cada vector uno por uno
    for i in range(0, cantidad_vectores):
        print(f"- Vector #{i + 1}")  # Indicar el número de vector
        vectores_incognita.append(input_vector(dimension))  # Leer el vector

    # Ingresar el vector resultado
    print("- Vector Resultado")
    vector_resultado: Vector = input_vector(dimension)

    # Calcular la combinación lineal
    combinacion_lineal(dimension, vectores_incognita, vector_resultado)

# -------------------------------
# Menú para resolver ecuaciones matriciales AX = B
# -------------------------------


def menu_ecuacion_matricial():
    """
    Menú interactivo para resolver ecuaciones matriciales de la forma AX = B.
    Permite al usuario ingresar la matriz cuadrada A y la matriz B.
    Utiliza la función resolver_ecuacion_matricial para mostrar la solución.
    """
    print("--- RESOLUCIÓN DE ECUACIÓN MATRICIAL AX = B ---")  # Título del menú

    # Leer tamaño de la matriz cuadrada A
    n = safe_input("Tamaño de la matriz cuadrada A (n): ", int)
    print("Ingrese la matriz A:")  # Solicitar matriz A
    A = input_matriz(n, n)         # Leer matriz A

    # Leer número de columnas de la matriz B
    m = safe_input("Número de columnas de la matriz B (m): ", int)
    # Solicitar matriz B
    print("Ingrese la matriz B (debe tener {} filas):".format(n))
    B = input_matriz(n, m)         # Leer matriz B

    # Resolver la ecuación matricial AX = B
    try:
        X = resolver_ecuacion_matricial(A, B)  # Calcular la solución
        print("\nSolución encontrada:")
        print(X)  # Mostrar la solución
    except Exception as e:
        print("Error:", str(e))  # Mostrar error si ocurre

# -------------------------------
# Menú para mostrar y verificar propiedades algebraicas de ℝⁿ
# -------------------------------


def menu_propiedades_algebraicas():
    """
    Menú interactivo para mostrar y verificar las propiedades algebraicas de ℝⁿ:
    - Suma de vectores
    - Multiplicación por escalar
    - Propiedad conmutativa
    - Propiedad asociativa
    - Existencia de vector cero
    - Existencia de vector opuesto
    """
    print("--- PROPIEDADES ALGEBRAICAS DE ℝⁿ ---")  # Título del menú
    print("1. Suma de vectores")
    print("2. Multiplicación por escalar")
    print("3. Verificar conmutativa")
    print("4. Verificar asociativa")
    print("5. Verificar existencia de vector cero")
    print("6. Verificar existencia de vector opuesto")
    print("7. <- Volver")
    opcion = safe_input("> ", funcion=int)  # Leer opción del usuario

    # Suma de dos vectores
    if opcion == 1:
        dim = safe_input("Dimensión de los vectores: ", funcion=int)
        print("- Vector A")
        vA = input_vector(dim)  # Leer vector A
        print("- Vector B")
        vB = input_vector(dim)  # Leer vector B
        resultado = suma_vectores(vA, vB)  # Calcular suma
        print(f"\nA + B = {resultado}\n")  # Mostrar resultado

    # Multiplicación de un vector por un escalar
    elif opcion == 2:
        dim = safe_input("Dimensión del vector: ", funcion=int)
        print("- Vector")
        v = input_vector(dim)  # Leer vector
        escalar = input_numero("Escalar: ")  # Leer escalar
        resultado = vector_por_escalar(v, escalar)  # Calcular producto
        print(f"\n{escalar} · {v} = {resultado}\n")  # Mostrar resultado

    # Verificar propiedad conmutativa: A + B = B + A
    elif opcion == 3:
        dim = safe_input("Dimensión de los vectores: ", funcion=int)
        print("- Vector A")
        vA = input_vector(dim)  # Leer vector A
        print("- Vector B")
        vB = input_vector(dim)  # Leer vector B
        suma1 = suma_vectores(vA, vB)  # Calcular A + B
        suma2 = suma_vectores(vB, vA)  # Calcular B + A
        print(f"\nA + B = {suma1}")
        print(f"B + A = {suma2}")
        # Verificar si son iguales
        print("¿Conmutativa?:", "Sí" if suma1.componentes ==
              suma2.componentes else "No")

    # Verificar propiedad asociativa: (A + B) + C = A + (B + C)
    elif opcion == 4:
        dim = safe_input("Dimensión de los vectores: ", funcion=int)
        print("- Vector A")
        vA = input_vector(dim)  # Leer vector A
        print("- Vector B")
        vB = input_vector(dim)  # Leer vector B
        print("- Vector C")
        vC = input_vector(dim)  # Leer vector C
        suma1 = suma_vectores(suma_vectores(vA, vB), vC)  # Calcular (A+B)+C
        suma2 = suma_vectores(vA, suma_vectores(vB, vC))  # Calcular A+(B+C)
        print(f"\n(A + B) + C = {suma1}")
        print(f"A + (B + C) = {suma2}")
        # Verificar si son iguales
        print("¿Asociativa?:", "Sí" if suma1.componentes ==
              suma2.componentes else "No")

    # Verificar existencia de vector cero: A + 0 = A
    elif opcion == 5:
        dim = safe_input("Dimensión del vector: ", funcion=int)
        print("- Vector A")
        vA = input_vector(dim)  # Leer vector A
        cero = Vector([0]*dim)  # Crear vector cero
        print(f"Vector Cero: {cero}")
        suma = suma_vectores(vA, cero)  # Calcular A + 0
        print(f"\nA + 0 = {suma}")
        # Verificar si es igual a A
        print("¿Existe vector cero?:", "Sí" if suma.componentes ==
              vA.componentes else "No")

    # Verificar existencia de vector opuesto: A + (-A) = 0
    elif opcion == 6:
        dim = safe_input("Dimensión del vector: ", funcion=int)
        print("- Vector A")
        vA = input_vector(dim)  # Leer vector A
        opuesto = vector_por_escalar(vA, -1)  # Calcular -A
        print(f"Vector Opuesto: {opuesto}")
        suma = suma_vectores(vA, opuesto)  # Calcular A + (-A)
        print(f"\nA + (-A) = {suma}")
        # Verificar si el resultado es el vector cero (tolerancia flotante)
        print("¿Existe vector opuesto?:", "Sí" if all(
            (x == 0) for x in suma.componentes) else "No")

    # Volver al menú principal
    elif opcion == 7:
        return


def menu_matriz_por_vector():
    dim = safe_input("Dimensión del vector: ", funcion=int)

    filas = safe_input("Filas de la Matriz: ", funcion=int)

    print("- Matriz")
    mat = input_matriz(filas, dim)

    print("- Vector")
    vA = input_vector(dim)

    result = matriz_por_vector(mat, vA)
    print(f"Resultado: {result}")


def menu_dependencia_lineal():
    """
    Menú interactivo para determinar si un conjunto de vectores es linealmente dependiente o independiente.
    Reutiliza input_vector para ingresar múltiples vectores en un loop.
    Llama a dependencia_lineal para resolver.
    """
    print("\n--- DEPENDENCIA E INDEPENDENCIA LINEAL ---")
    dimension: int = safe_input(
        "Dimensión de los vectores (ℝⁿ): ", funcion=int)
    num_vectores: int = safe_input(
        "Número de vectores en el conjunto: ", funcion=int)
    vectores: list[Vector] = []
    for i in range(1, num_vectores + 1):
        print(f"\n- Vector #{i}")
        vectores.append(input_vector(dimension))
    dependencia_lineal(dimension, vectores)


def menu_matrices():
    def menu_sumar_matrices():
        print("Matriz #1:")
        filas = safe_input("Numero de filas: ", funcion=int)
        columnas = safe_input("Numero de columnas: ", funcion=int)
        mat1 = input_matriz(filas, columnas)

        print("Matriz #2:")
        filas = safe_input("Numero de filas: ", funcion=int)
        columnas = safe_input("Numero de columnas: ", funcion=int)
        mat2 = input_matriz(filas, columnas)

        try:
            print(f"Resultado: \n{suma_matrices(mat1, mat2)}")
        except Exception as err:
            print(f"No se puede realizar la operación, {err}")

    def menu_restar_matrices():
        print("Matriz #1:")
        filas = safe_input("Numero de filas: ", funcion=int)
        columnas = safe_input("Numero de columnas: ", funcion=int)
        mat1 = input_matriz(filas, columnas)

        print("Matriz #2:")
        filas = safe_input("Numero de filas: ", funcion=int)
        columnas = safe_input("Numero de columnas: ", funcion=int)
        mat2 = input_matriz(filas, columnas)

        try:
            print(f"Resultado: \n{resta_matrices(mat1, mat2)}")
        except Exception as err:
            print(f"No se puede realizar la operación, {err}")

    def menu_matriz_por_escalar():
        print("Matriz:")
        filas = safe_input("Numero de filas: ", funcion=int)
        columnas = safe_input("Numero de columnas: ", funcion=int)
        mat = input_matriz(filas, columnas)

        print("Escalar: ")
        escalar = input_numero("Ingrese el escalar: ")
        print(
            f"Resultado:\n{matriz_por_escalar(mat, escalar, calcprint=True)}")

    def menu_multiplicar_matrices():
        print("Matriz #1:")
        filas = safe_input("Numero de filas: ", funcion=int)
        columnas = safe_input("Numero de columnas: ", funcion=int)
        mat1 = input_matriz(filas, columnas)

        print("Matriz #2:")
        filas = safe_input("Numero de filas: ", funcion=int)
        columnas = safe_input("Numero de columnas: ", funcion=int)
        mat2 = input_matriz(filas, columnas)

        try:
            print(
                f"Resultado: \n{multiplicar_matrices(mat1, mat2, calcprint=True)}")
        except Exception as err:
            print(f"No se puede realizar la operación, {err}")

    def menu_trasponer_matriz():
        print("Matriz:")
        filas = safe_input("Numero de filas: ", funcion=int)
        columnas = safe_input("Numero de columnas: ", funcion=int)
        mat = input_matriz(filas, columnas)

        print(f"Resultado: \n{transponer_matriz(mat, calcprint=True)}")

    def menu_matriz_invertida():
        print("Matriz:")
        n = safe_input("Tamaño de la matriz (n x n): ", funcion=int)
        mat = input_matriz(n, n)

        try:
            calcular_inversa(mat, n)
        except Exception as err:
            print(f"No se puede realizar la operación, {err}")

    def menu_matriz_invertida_adjunta():
        print("Matriz:")
        n = safe_input("Tamaño de la matriz (n x n): ", funcion=int)
        mat = input_matriz(n, n)

        try:
            inv = inversion_por_adjunta(mat, calcprint=True)
            print(f"La matriz inversa es:\n{inv}")
        except Exception as err:
            print(f"No se puede realizar la operación, {err}")

    def menu_determinante_sarrus():
        print("Matriz:")
        n = safe_input("Tamaño de la matriz (n x n): ", funcion=int)
        mat = input_matriz(n, n)

        try:
            det = determinante_por_sarrus(mat, calcprint=True)
            print(f"Determinante: {det}")
            if det == 0:
                print(f"La matriz es singular y no invertible.")
            else:
                print(f"La matriz es no singular e invertible.")
        except Exception as err:
            print(f"No se puede realizar la operación, {err}")

    def menu_determinante_cofactores():
        print("Matriz:")
        n = safe_input("Tamaño de la matriz (n x n): ", funcion=int)
        mat = input_matriz(n, n)

        try:
            det = determinante_por_cofactores(mat, calcprint=True)
            if det == 0:
                print(f"La matriz es singular y no invertible.")
            else:
                print(f"La matriz es no singular e invertible.")
        except Exception as err:
            print(f"No se puede realizar la operación, {err}")
        # try:
        #     print(f"Resultado: \n{matriz_inversa(mat)}")
        # except Exception as err:
        #     print(f"No se puede realizar la operación, {err}")

    menu = Menu([
        ("Suma de matrices", menu_sumar_matrices),
        ("Resta de matrices", menu_restar_matrices),
        ("Matriz por escalar", menu_matriz_por_escalar),
        ("Multiplicar matrices", menu_multiplicar_matrices),
        ("Trasponer Matriz", menu_trasponer_matriz),
        ("Matriz Inversa (Gauss-Jordan)", menu_matriz_invertida),
        ("Matriz Inversa (Por Adjunta)", menu_matriz_invertida_adjunta),
        ("Calcular Determinante (sarrus)", menu_determinante_sarrus),
        ("Calcular Determinante (co-factores)", menu_determinante_cofactores),
        ("<- Volver", lambda: None)
    ])

    menu.showget()


def menu_propiedades_matrices():

    def propiedad_suma_conmutativa():
        print("Propiedad: A + B = B + A")
        filas = safe_input("Filas: ", int)
        columnas = safe_input("Columnas: ", int)
        print("Matriz A:")
        A = input_matriz(filas, columnas)
        print("Matriz B:")
        B = input_matriz(filas, columnas)
        suma1 = suma_matrices(A, B)
        suma2 = suma_matrices(B, A)
        print(f"A + B =\n{suma1}")
        print(f"B + A =\n{suma2}")
        print("¿Conmutativa?:", "Sí" if suma1 == suma2 else "No")

    def propiedad_suma_asociativa():
        print("Propiedad: (A + B) + C = A + (B + C)")
        filas = safe_input("Filas: ", int)
        columnas = safe_input("Columnas: ", int)
        print("Matriz A:")
        A = input_matriz(filas, columnas)
        print("Matriz B:")
        B = input_matriz(filas, columnas)
        print("Matriz C:")
        C = input_matriz(filas, columnas)
        suma1 = suma_matrices(suma_matrices(A, B), C)
        suma2 = suma_matrices(A, suma_matrices(B, C))
        print(f"(A + B) + C =\n{suma1}")
        print(f"A + (B + C) =\n{suma2}")
        print("¿Asociativa?:", "Sí" if suma1 == suma2 else "No")

    def propiedad_elemento_neutro():
        print("Propiedad: A + 0 = A")
        filas = safe_input("Filas: ", int)
        columnas = safe_input("Columnas: ", int)
        print("Matriz A:")
        A = input_matriz(filas, columnas)
        cero = Matriz(filas, columnas)
        suma = suma_matrices(A, cero)
        print(f"A + 0 =\n{suma}")
        print("¿Elemento neutro?:", "Sí" if suma == A else "No")

    def propiedad_distributiva_escalar_suma():
        print("Propiedad: r(A + B) = rA + rB")
        filas = safe_input("Filas: ", int)
        columnas = safe_input("Columnas: ", int)
        print("Matriz A:")
        A = input_matriz(filas, columnas)
        print("Matriz B:")
        B = input_matriz(filas, columnas)
        r = input_numero("Escalar r: ")
        izquierda = matriz_por_escalar(suma_matrices(A, B), r)
        derecha = suma_matrices(matriz_por_escalar(
            A, r), matriz_por_escalar(B, r))
        print(f"r(A + B) =\n{izquierda}")
        print(f"rA + rB =\n{derecha}")
        print("¿Distributiva?:", "Sí" if izquierda == derecha else "No")

    def propiedad_distributiva_suma_escalars():
        print("Propiedad: (r + s)A = rA + sA")
        filas = safe_input("Filas: ", int)
        columnas = safe_input("Columnas: ", int)
        print("Matriz A:")
        A = input_matriz(filas, columnas)
        r = input_numero("Escalar r: ")
        s = input_numero("Escalar s: ")
        izquierda = matriz_por_escalar(A, r + s)
        derecha = suma_matrices(matriz_por_escalar(
            A, r), matriz_por_escalar(A, s))
        print(f"(r + s)A =\n{izquierda}")
        print(f"rA + sA =\n{derecha}")
        print("¿Distributiva?:", "Sí" if izquierda == derecha else "No")

    def propiedad_compatibilidad_escalars():
        print("Propiedad: r(sA) = (rs)A")
        filas = safe_input("Filas: ", int)
        columnas = safe_input("Columnas: ", int)
        print("Matriz A:")
        A = input_matriz(filas, columnas)
        r = input_numero("Escalar r: ")
        s = input_numero("Escalar s: ")
        izquierda = matriz_por_escalar(matriz_por_escalar(A, s), r)
        derecha = matriz_por_escalar(A, r * s)
        print(f"r(sA) =\n{izquierda}")
        print(f"(rs)A =\n{derecha}")
        print("¿Compatibilidad?:", "Sí" if izquierda == derecha else "No")

    def propiedad_doble_transposicion():
        print("Propiedad: (Aᵗ)ᵗ = A")
        filas = safe_input("Filas: ", int)
        columnas = safe_input("Columnas: ", int)
        print("Matriz A:")
        A = input_matriz(filas, columnas)
        transpuesta = transponer_matriz(A)
        doble = transponer_matriz(transpuesta)
        print(f"(Aᵗ)ᵗ =\n{doble}")
        print("¿Igual a A?:", "Sí" if doble == A else "No")

    def propiedad_transposicion_suma():
        print("Propiedad: (A + B)ᵗ = Aᵗ + Bᵗ")
        filas = safe_input("Filas: ", int)
        columnas = safe_input("Columnas: ", int)
        print("Matriz A:")
        A = input_matriz(filas, columnas)
        print("Matriz B:")
        B = input_matriz(filas, columnas)
        izquierda = transponer_matriz(suma_matrices(A, B))
        derecha = suma_matrices(transponer_matriz(A), transponer_matriz(B))
        print(f"(A + B)ᵗ =\n{izquierda}")
        print(f"Aᵗ + Bᵗ =\n{derecha}")
        print("¿Iguales?:", "Sí" if izquierda == derecha else "No")

    def propiedad_transposicion_resta():
        print("Propiedad: (A - B)ᵗ = Aᵗ - Bᵗ")
        filas = safe_input("Filas: ", int)
        columnas = safe_input("Columnas: ", int)
        print("Matriz A:")
        A = input_matriz(filas, columnas)
        print("Matriz B:")
        B = input_matriz(filas, columnas)
        izquierda = transponer_matriz(resta_matrices(A, B))
        derecha = resta_matrices(transponer_matriz(A), transponer_matriz(B))
        print(f"(A - B)ᵗ =\n{izquierda}")
        print(f"Aᵗ - Bᵗ =\n{derecha}")
        print("¿Iguales?:", "Sí" if izquierda == derecha else "No")

    def propiedad_transposicion_escalar():
        print("Propiedad: r(A)ᵗ = rAᵗ")
        filas = safe_input("Filas: ", int)
        columnas = safe_input("Columnas: ", int)
        print("Matriz A:")
        A = input_matriz(filas, columnas)
        r = input_numero("Escalar r: ")
        izquierda = transponer_matriz(matriz_por_escalar(A, r))
        derecha = matriz_por_escalar(transponer_matriz(A), r)
        print(f"r(A)ᵗ =\n{izquierda}")
        print(f"rAᵗ =\n{derecha}")
        print("¿Iguales?:", "Sí" if izquierda == derecha else "No")

    def propiedad_transposicion_producto():
        print("Propiedad: (AB)ᵗ = BᵗAᵗ")
        filasA = safe_input("Filas de A: ", int)
        columnasA = safe_input("Columnas de A: ", int)
        print("Matriz A:")
        A = input_matriz(filasA, columnasA)
        filasB = columnasA
        columnasB = safe_input("Columnas de B: ", int)
        print("Matriz B:")
        B = input_matriz(filasB, columnasB)

        AB = multiplicar_matrices(A, B)
        print(f"AB = \n{AB}")
        izquierda = transponer_matriz(AB)
        AT = transponer_matriz(A)
        BT = transponer_matriz(B)
        derecha = multiplicar_matrices(
            AT, BT)
        print(f"(AB)ᵗ =\n{izquierda}")

        print(f"Bᵗ = \n{BT}")
        print(f"Aᵗ = \n{AT}")
        print(f"BᵗAᵗ =\n{derecha}")
        print("¿Iguales?:", "Sí" if izquierda == derecha else "No")

    def propiedad_distributiva_escalar_suma_traspuesta():
        print("Propiedad: r(A + B)ᵗ = rAᵗ + rBᵗ")
        filas = safe_input("Filas: ", int)
        columnas = safe_input("Columnas: ", int)
        print("Matriz A:")
        A = input_matriz(filas, columnas)
        print("Matriz B:")
        B = input_matriz(filas, columnas)
        r = input_numero("Escalar r: ")
        AtBt = transponer_matriz(suma_matrices(A, B))
        rAt = transponer_matriz(matriz_por_escalar(A, r))
        rBt = transponer_matriz(matriz_por_escalar(B, r))
        print(f"Aᵗ + Bᵗ: \n{AtBt}")
        izquierda = matriz_por_escalar(AtBt, r)
        print(f"r(Aᵗ + Bᵗ): \n{matriz_por_escalar(AtBt, r)}")
        print(f"rAᵗ: \n{rAt}")
        print(f"rBᵗ: \n{rBt}")
        print(f"rAᵗ + rBᵗ: \n{suma_matrices(rAt, rBt)}")
        derecha = suma_matrices(rAt, rBt)
        print("¿Iguales?:", "Sí" if izquierda == derecha else "No")

    def propiedad_intercambio_determinante():
        n = safe_input("Tamaño de la matriz (nxn): ", int)
        if n < 2:
            print(f"No es posible demostrar la propiedad con una matriz de 1x1")

        m = input_matriz(n, n)

        det_a = determinante_por_cofactores(m, calcprint=True)
        intercambiar_fila(m, 1, 2)
        print(f"Intercambiando fila 1 y fila 2...")
        det_b = determinante_por_cofactores(m, calcprint=True)

        print(f"Da = -Db? {"Si" if det_a == -det_b else "No"}")

    def propiedad_multiplicacion_determinante():
        n = safe_input("Tamaño de la matriz (nxn): ", int)
        if n < 2:
            print(f"No es posible demostrar la propiedad con una matriz de 1x1")

        m = input_matriz(n, n)
        k = input_numero("Escalar k: ")

        det_a = determinante_por_cofactores(m, calcprint=True)
        escalar_fila(m, 1, k)

        print(f"Escalando fila 1 por {k}")
        det_b = determinante_por_cofactores(m, calcprint=True)

        print(f"k * Da = Db? {"Si" if k * det_a == det_b else "No"}")

    def propiedad_multiplicativa_determinante():
        n = safe_input("Tamaño de la matriz (nxn): ", int)

        A = input_matriz(n, n)
        B = input_matriz(n, n)

        det_a = determinante_por_cofactores(A, calcprint=True)
        det_b = determinante_por_cofactores(B, calcprint=True)

        AB = multiplicar_matrices(A, B)
        print(f"A * B:\n{AB}")
        det_ab = determinante_por_cofactores(AB, calcprint=True)

        print(f"Da = {det_a}\nDb = {det_b}\nDab = {det_ab}")
        print(f"Da * Db = Dab? {"Si" if det_a * det_b == det_ab else "No"}")

    menu = Menu([
        ("Suma conmutativa (A + B = B + A)", propiedad_suma_conmutativa),
        ("Suma asociativa ((A + B) + C = A + (B + C))", propiedad_suma_asociativa),
        ("Elemento neutro (A + 0 = A)", propiedad_elemento_neutro),
        ("Distributiva escalar sobre suma (r(A + B) = rA + rB)",
         propiedad_distributiva_escalar_suma),
        ("Distributiva suma de escalares ((r + s)A = rA + sA)",
         propiedad_distributiva_suma_escalars),
        ("Compatibilidad de escalares (r(sA) = (rs)A)",
         propiedad_compatibilidad_escalars),
        ("Doble transposición ((Aᵗ)ᵗ = A)", propiedad_doble_transposicion),
        ("Transposición de suma ((A + B)ᵗ = Aᵗ + Bᵗ)", propiedad_transposicion_suma),
        ("Transposición de resta ((A - B)ᵗ = Aᵗ-- Bᵗ)",
         propiedad_transposicion_resta),
        ("Transposición de producto por escalar ((rA)ᵗ = rAᵗ)",
         propiedad_transposicion_escalar),
        ("Transposición de producto de matrices ((AB)ᵗ = BᵗAᵗ)",
         propiedad_transposicion_producto),
        ("Distributiva escalar sobre suma traspuesta (r(A + B)ᵗ = rAᵗ + rBᵗ",
         propiedad_distributiva_escalar_suma_traspuesta),
        ("Cambio de signo del determinante mediante cambio de fila",
         propiedad_intercambio_determinante),
        ("Multiplicación del determinante mediante multiplicación de fila",
         propiedad_multiplicacion_determinante),
        ("Propiedad multiplicativa del determinante",
         propiedad_multiplicativa_determinante),
        ("<- Volver", lambda: None)
    ])
    menu.showget()


# -------------------------------
# Programa principal (CLI)
# -------------------------------
if __name__ == "__main__":
    # Mensaje de bienvenida y descripción
    print("--- LINAL CLI ---\n")
    print("Esta aplicacion es la version CLI (Command Line Interface)")
    print("Tiene diversas aplicaciones y funciones, que en un futuro se conectaran a una interfaz grafica.\n")

    main_menu = Menu(
        [
            ("Calculadora de Sistema de Ecuaciones (Gauss-Jordan)",
             menu_sistema_ecuaciones),
            ("Calculadora de Sistema de Ecuaciones (Cramer)",
             menu_sistema_ecuaciones_cramer),
            ("Calculadora de Combinacion Lineal", menu_combinacion_lineal),
            ("Propiedades algebraicas de ℝⁿ", menu_propiedades_algebraicas),
            ("Ecuación matricial", menu_ecuacion_matricial),
            ("Matriz por vector", menu_matriz_por_vector),
            ("Dependencia lineal", menu_dependencia_lineal),
            ("Operaciones con Matrices", menu_matrices),
            ("Propiedades de Matrices", menu_propiedades_matrices),
            ("<- Salir", lambda: exit(0))
        ]
    )

    # Menú principal interactivo
    while True:
        main_menu.showget()
